import asyncio
import functools
import gc
import importlib
import logging
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from json import dumps as stringify
from typing import Any, Dict, List, Optional, TypedDict, Type, Literal

# pylint: disable-next=unused-import
import cv2  # type: ignore
# import openai_async
import pymysql
from sanic import Sanic
from sanic.log import access_logger, logger
from sanic.request import Request
from sanic.response import json
from sanic.server.protocols.websocket_protocol import WebSocketProtocol
from sanic_cors import CORS

from base_types import NodeId
from nm_graph.cache import OutputCache
from nm_graph.json import JsonNode, parse_json
from nm_graph.optimize import optimize
from events import EventChannel, ExecutionErrorData, UIEventChannel, ToUIOutputMessage, UIEvtChannelSchema, \
    UIEvtChannelKind, FromUIOutputMessage
from nodes.group import Group
from nodes.node_factory import NodeFactory
from nodes.nodes.builtin_categories import category_order
from nodes.utils.exec_options import (
    JsonExecutionOptions,
    parse_execution_options,
    set_execution_options,
)
from process import (
    Executor,
    NodeExecutionError,
    Output,
    compute_broadcast,
    timed_supplier,
    to_output,
)
from progress import Aborted
from response import (
    alreadyRunningResponse,
    errorResponse,
    noExecutorResponse,
    successResponse,
)

import pandas as pd
import json as json_lib

from src.nodes.io.outputs import BaseOutput


class AppContext:
    def __init__(self):
        self.executor: Optional[Executor] = None
        self.cache: Dict[NodeId, Output] = dict()
        # This will be initialized by setup_queue.
        # This is necessary because we don't know Sanic's event loop yet.
        self.sse_channel: EventChannel = None  # type: ignore
        # should be in app context really?
        self.to_ui_channel: UIEventChannel = None
        self.from_ui_channel: UIEventChannel = None

        self.pool = ThreadPoolExecutor(max_workers=4)

    @staticmethod
    def get(app_instance: Sanic) -> "AppContext":
        assert isinstance(app_instance.ctx, AppContext)
        return app_instance.ctx


app = Sanic("MachinesStudio", ctx=AppContext())
app.config.REQUEST_TIMEOUT = sys.maxsize
app.config.RESPONSE_TIMEOUT = sys.maxsize
CORS(app)

missing_node_count = 0
categories = set()
missing_categories = set()
missing_module_errors = set()

# Dynamically import all nodes
for root, dirs, files in os.walk(
        os.path.join(os.path.dirname(__file__), "nodes", "nodes")
):
    for file in files:
        if file.endswith(".py") and not file.startswith("_"):
            module = os.path.relpath(
                os.path.join(root, file), os.path.dirname(__file__)
            )
            module = module.replace(os.path.sep, ".")[:-3]
            try:
                importlib.import_module(f"{module}", package=None)
            except ImportError as e:
                missing_node_count += 1
                logger.debug(f"Failed to import {module}: {e}")
                missing_module_errors.add(str(e))

                # Turn path into __init__.py path
                init_module = module.split(".")
                init_module[-1] = "__init__"
                init_module = ".".join(init_module)
                try:
                    category = getattr(importlib.import_module(init_module), "category")
                    missing_categories.add(category.name)
                except ImportError as ie:
                    logger.info(ie)
                except Exception as oe:
                    logger.error(
                        f"A critical error occurred when importing module {init_module}: {oe}"
                    )
            except Exception as e:
                logger.error(
                    f"A critical error occurred when importing module {module}: {e}"
                )
        # Load categories from __init__.py files
        elif file.endswith(".py") and file == ("__init__.py"):
            module = os.path.relpath(
                os.path.join(root, file), os.path.dirname(__file__)
            )
            module = module.replace(os.path.sep, ".")[:-3]
            try:
                # TODO: replace the category system with a dynamic factory
                category = getattr(importlib.import_module(module), "category")
                categories.add(category)
            except:
                pass

if len(missing_module_errors) > 0:
    logger.warning(
        f"Failed to import {missing_node_count} nodes. "
        f"Missing categories: {missing_categories}. "
        f"Missing modules: {missing_module_errors}"
    )

categories = sorted(
    list(categories), key=lambda category: category_order.index(category.name)
)


class SSEFilter(logging.Filter):
    def filter(self, record):
        return not (record.request.endswith("/sse") and record.status == 200)  # type: ignore


class UISSEFilter(logging.Filter):
    def filter(self, record):
        return not (record.request.endswith("/ui_sse") and record.status == 200)  # type: ignore


class ZeroCounter:
    def __init__(self) -> None:
        self.count = 0

    async def wait_zero(self) -> None:
        while self.count != 0:
            await asyncio.sleep(0.01)

    def __enter__(self):
        self.count += 1

    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        self.count -= 1


runIndividualCounter = ZeroCounter()

access_logger.addFilter(SSEFilter())
access_logger.addFilter(UISSEFilter())


@app.route("/nodes")
async def nodes(_):
    """Gets a list of all nodes as well as the node information"""
    registry = NodeFactory.get_registry()
    logger.debug(categories)

    # sort nodes in category order
    sorted_registry = sorted(
        registry.items(),
        key=lambda x: category_order.index(NodeFactory.get_node(x[0]).category.name),  # fixme: dirty hack
    )
    node_list = []
    for schema_id, _node_class in sorted_registry:
        node_object = NodeFactory.get_node(schema_id)
        node_dict = {
            "schemaId": schema_id,
            "name": node_object.name,
            "category": node_object.category.name,
            "inputs": [x.toDict() for x in node_object.inputs],
            "outputs": [x.toDict() for x in node_object.outputs],
            "groupLayout": [
                g.toDict() if isinstance(g, Group) else g
                for g in node_object.group_layout
            ],
            "description": node_object.description,
            "icon": node_object.icon,
            "subcategory": node_object.sub,
            "nodeType": node_object.type,
            "hasSideEffects": node_object.side_effects,
            "deprecated": node_object.deprecated,
        }
        if node_object.type == "iterator":
            node_dict["defaultNodes"] = node_object.get_default_nodes()  # type: ignore
        node_list.append(node_dict)
    return json(
        {
            "nodes": node_list,
            "categories": [x.toDict() for x in categories],
            "categoriesMissingNodes": list(missing_categories),
        }
    )


class RunRequest(TypedDict):
    data: List[JsonNode]
    options: JsonExecutionOptions
    sendBroadcastData: bool


@app.route("/run", methods=["POST"])
async def run(request: Request):
    """
    Runs the provided nodes.
    todo: the nodes with websocket ui should register
    """
    ctx = AppContext.get(request.app)

    if ctx.executor:
        message = "Cannot run another executor while the first one is still running."
        logger.warning(message)
        return json(alreadyRunningResponse(message), status=500)

    try:
        # wait until all previews are done
        await runIndividualCounter.wait_zero()

        full_data: RunRequest = dict(request.json)  # type: ignore
        logger.debug(full_data)
        graph, inputs = parse_json(full_data["data"])
        # iterate through the dict
        for node_id, node in graph.nodes.items():
            # the outputs here store the kinds of messages allowed
            node = node.get_node()
            node.set_event_loop(app.loop)
            node_outputs: List[BaseOutput] = node.get_outputs()
            for output in node_outputs:
                output.provide_channel_to_output(ctx.to_ui_channel)
                output.provide_channel_for_input(ctx.from_ui_channel)

        # todo: node_outputs, get channel from node_instance and connect it to the sse/websocket
        #

        logger.info("Running new executor...")
        exec_opts = parse_execution_options(full_data["options"])
        set_execution_options(exec_opts)
        logger.debug(f"Using device: {exec_opts.full_device}")
        # the executor will create the subscriptions for the reactive i/o
        executor = Executor(
            graph,
            inputs,
            full_data["sendBroadcastData"],
            app.loop,
            ctx.sse_channel,
            ctx.pool,
            parent_cache=OutputCache(static_data=ctx.cache.copy()),
        )
        try:
            ctx.executor = executor
            # todo: run should be blocking
            await executor.run()
        except Aborted:
            pass
        finally:
            ctx.executor = None
            gc.collect()
        await ctx.sse_channel.put(
            {"event": "finish", "data": {"message": "Successfully ran nodes!"}}
        )
        return json(successResponse("Successfully ran nodes!"), status=200)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        logger.error(traceback.format_exc())

        error: ExecutionErrorData = {
            "message": "Error running nodes!",
            "source": None,
            "exception": str(exception),
        }
        if isinstance(exception, NodeExecutionError):
            error["source"] = {
                "nodeId": exception.node.id,
                "schemaId": exception.node.schema_id,
                "inputs": exception.inputs,
            }

        await ctx.sse_channel.put({"event": "execution-error", "data": error})
        return json(errorResponse("Error running nodes!", exception), status=500)


class RunIndividualRequest(TypedDict):
    id: NodeId
    inputs: List[Any]
    schemaId: str
    options: JsonExecutionOptions


@app.route("/run/individual", methods=["POST"])
async def run_individual(request: Request):
    """Runs a single node"""
    logger.info("Running individual node...")
    ctx = AppContext.get(request.app)
    try:
        full_data: RunIndividualRequest = dict(request.json)  # type: ignore
        if ctx.cache.get(full_data["id"], None) is not None:
            del ctx.cache[full_data["id"]]
        logger.debug(full_data)
        exec_opts = parse_execution_options(full_data["options"])
        set_execution_options(exec_opts)
        logger.debug(f"Using device: {exec_opts.full_device}")
        # Create node based on given category/name information
        node_instance = NodeFactory.get_node(full_data["schemaId"])

        # Enforce that all inputs match the expected input schema
        enforced_inputs = []
        if node_instance.type == "iteratorHelper":
            enforced_inputs = full_data["inputs"]
        else:
            node_inputs = node_instance.inputs
            for idx, node_input in enumerate(full_data["inputs"]):
                enforced_inputs.append(node_inputs[idx].enforce_(node_input))

        with runIndividualCounter:
            # Run the node and pass in inputs as args
            run_func = functools.partial(node_instance.run, *full_data["inputs"])
            raw_output, execution_time = await app.loop.run_in_executor(
                None, timed_supplier(run_func)
            )
            output = to_output(raw_output, node_instance)

            # Cache the output of the node
            ctx.cache[full_data["id"]] = output
        # Broadcast the output from the individual run
        node_outputs = node_instance.outputs
        if len(node_outputs) > 0:
            data, types = compute_broadcast(output, node_outputs)
            await ctx.sse_channel.put(
                {
                    "event": "node-finish",
                    "data": {
                        "finished": [],
                        "nodeId": full_data["id"],
                        "executionTime": execution_time,
                        "data": data,
                        "types": types,
                        "progressPercent": None,
                    },
                }
            )
        del node_instance, run_func
        gc.collect()
        return json({"success": True, "data": None})
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


@app.route("/clearcache/individual", methods=["POST"])
async def clear_cache_individual(request: Request):
    ctx = AppContext.get(request.app)
    try:
        full_data = dict(request.json)  # type: ignore
        if ctx.cache.get(full_data["id"], None) is not None:
            del ctx.cache[full_data["id"]]
        return json({"success": True, "data": None})
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


@app.get("/sse")
async def sse(request: Request):
    ctx = AppContext.get(request.app)
    headers = {"Cache-Control": "no-cache"}
    response = await request.respond(headers=headers, content_type="text/event-stream")
    while True:
        message = await ctx.sse_channel.get()
        if response is not None:
            await response.send(f"event: {message['event']}\n")
            await response.send(f"data: {stringify(message['data'])}\n\n")


@app.after_server_start
async def setup_queue(sanic_app: Sanic, _):
    # todo: set the ui_queues here
    AppContext.get(sanic_app).sse_channel = EventChannel()
    AppContext.get(sanic_app).to_ui_channel = UIEventChannel('ui_uplink', UIEvtChannelKind.UPLINK)
    AppContext.get(sanic_app).from_ui_channel = UIEventChannel('ui_downlink', UIEvtChannelKind.DOWNLINK)


@app.route("/pause", methods=["POST"])
async def pause(request: Request):
    """Pauses the current execution"""
    ctx = AppContext.get(request.app)

    if not ctx.executor:
        message = "No executor to pause"
        logger.warning(message)
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to pause...")
        ctx.executor.pause()
        return json(successResponse("Successfully paused execution!"), status=200)
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(errorResponse("Error pausing execution!", exception), status=500)


@app.route("/resume", methods=["POST"])
async def resume(request: Request):
    """Pauses the current execution"""
    ctx = AppContext.get(request.app)

    if not ctx.executor:
        message = "No executor to resume"
        logger.warning(message)
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to resume...")
        ctx.executor.resume()
        return json(successResponse("Successfully resumed execution!"), status=200)
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(errorResponse("Error resuming execution!", exception), status=500)


@app.route("/kill", methods=["POST"])
async def kill(request: Request):
    """Kills the current execution"""
    ctx = AppContext.get(request.app)

    if not ctx.executor:
        message = "No executor to kill"
        logger.warning("No executor to kill")
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to kill...")
        ctx.executor.kill()
        while ctx.executor:
            await asyncio.sleep(0.0001)
        return json(successResponse("Successfully killed execution!"), status=200)
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(errorResponse("Error killing execution!", exception), status=500)


@app.route("/listgpus/ncnn", methods=["GET"])
async def list_ncnn_gpus(_request: Request):
    """Lists the available GPUs for NCNN"""
    try:
        # pylint: disable=import-outside-toplevel
        from ncnn_vulkan import ncnn

        result = []
        for i in range(ncnn.get_gpu_count()):
            result.append(ncnn.get_gpu_info(i).device_name())
        return json(result)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json([])


@app.route("/python-info", methods=["GET"])
async def python_info(_request: Request):
    version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    return json({"python": sys.executable, "version": version})


@app.websocket("/to_front_ui")
async def ui_sse(request: Request, ws):
    ctx = AppContext.get(request.app)

    while True:
        message: ToUIOutputMessage = await ctx.to_ui_channel.get()
        logger.info(f"Sending message to UI Finally: {message}")
        # todo: wait for some response depending on the message sent?
        # todo: use protobuf
        await ws.send(json_lib.dumps(message))


@app.websocket("/ui")
async def ui_ws(request: Request, ws):
    ctx = AppContext.get(request.app)

    async def send_to_ui():
        while True:
            message: ToUIOutputMessage = await ctx.to_ui_channel.get()
            logger.info(f"Sending message to UI Finally: {message}")
            await ws.send(json_lib.dumps(message))

    async def receive_from_ui():
        while True:
            try:
                # Receive message from the websocket
                raw_message = await ws.recv()
                # Deserialize the message
                message: FromUIOutputMessage = json_lib.loads(raw_message)
                logger.info(f"Received message from UI: {message}")

                # Put the message into the from_ui_channel
                await ctx.from_ui_channel.put(message)
            except Exception as e:
                logger.error(f"Error processing message from UI: {e}")
                break

    # Run the sending and receiving coroutines concurrently
    await asyncio.gather(send_to_ui(), receive_from_ui())


if __name__ == "__main__":
    try:
        port = int(sys.argv[1]) or 8000
    except:
        port = 8000
    app.update_config({"RESPONSE_TIMEOUT": 500, "KEEP_ALIVE_TIMEOUT": 500, "REQUEST_TIMEOUT": 500})
    app.run(port=port, protocol=WebSocketProtocol)

    if sys.argv[1] != "--no-run":
        app.run(port=port)
