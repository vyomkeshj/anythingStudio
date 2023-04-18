from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import TypedDict

from sanic.log import logger

from src.base_types import NodeId
from src.events import ToUIOutputMessage, UIMessageType
from ...io.outputs.chat_output import ChatOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as DatabaseCategory
import json as json_lib

import asyncio


class MsgFromUser(TypedDict):
    msg: str


class MsgFromChatbot(TypedDict):
    msg: str


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:database:chat_node")
class ChatQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Chat with your database."
        self.inputs = [
            TextLineInput("Schema"),
            TextLineInput("ModelName", default="gpt-3.5-turbo")
        ]
        self.chat_output = ChatOutput()
        self.outputs = [self.chat_output]

        # todo: communicate with ui using the channels in chat_output

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "ChatQ"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True
        self.schema = ""
        self.pool = ThreadPoolExecutor(max_workers=4)

    def run(self, prompt: str, use_model: str) -> str:
        """
        Run runs only once, so we can use it to initialize the machine, but we can put things on the event loop to run
        """
        logger.info(f"Running chat node with id: {self.node_id}")
        run_async_in_executor(self.chat_output, self.node_id)
        return json_lib.dumps({"database_schema": prompt, "use_model": use_model})

    async def run_loops(self):
        pass


def run_async_in_executor(base_output: ChatOutput, node_id: NodeId):
    send_event_loop = asyncio.new_event_loop()
    try:
        result = send_event_loop.run_until_complete(send_ui_event(base_output, node_id))
        return result
    finally:
        send_event_loop.close()


async def send_ui_event(chat_ui_out: ChatOutput, node_id: NodeId):
    # channel id is unique to the output
    channel_id = chat_ui_out.get_channel_id_by_name('msg_from_chatbot')
    message = MsgFromChatbot(msg="Hello from chatbot")

    out_message = ToUIOutputMessage(node_id=node_id,
                                    channel_id=channel_id,
                                    output_id=chat_ui_out.id,
                                    data=message,
                                    message_tag="msg_from_chatbot")

    await chat_ui_out.send_ui_event(event=out_message)
    await asyncio.sleep(10)
    await chat_ui_out.send_ui_event(event=out_message)
    logger.info("bye...")

