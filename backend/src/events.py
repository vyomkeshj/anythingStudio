import asyncio
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from base_types import InputId, NodeId, OutputId


class FinishData(TypedDict):
    message: str


class ImageInputInfo(TypedDict):
    width: int
    height: int
    channels: int


InputsDict = Dict[InputId, Union[str, int, float, ImageInputInfo, None]]


class ExecutionErrorSource(TypedDict):
    nodeId: NodeId
    schemaId: str
    inputs: InputsDict


class ExecutionErrorData(TypedDict):
    message: str
    exception: str
    source: Optional[ExecutionErrorSource]


class NodeFinishData(TypedDict):
    finished: List[NodeId]
    nodeId: NodeId
    executionTime: Optional[float]
    data: Optional[Dict[OutputId, Any]]
    types: Optional[Dict[OutputId, Any]]
    progressPercent: Optional[float]


class IteratorProgressUpdateData(TypedDict):
    percent: float
    iteratorId: NodeId
    running: Optional[List[NodeId]]


class ReactiveNodeUIMessage(TypedDict):
    message: str
    toNode: NodeId


class FinishEvent(TypedDict):
    event: Literal["finish"]
    data: FinishData


class ExecutionErrorEvent(TypedDict):
    event: Literal["execution-error"]
    data: ExecutionErrorData


class NodeFinishEvent(TypedDict):
    event: Literal["node-finish"]
    data: NodeFinishData


# todo: use this for reactive updates to ui?
class IteratorProgressUpdateEvent(TypedDict):
    event: Literal["iterator-progress-update"]
    data: IteratorProgressUpdateData


class ToUINodeMessage(TypedDict):
    event: Literal["ui-node-event"]
    node_id: NodeId
    data: IteratorProgressUpdateData


FromNodeEvent = Union[
    ToUINodeMessage,
    FinishEvent,
    ExecutionErrorEvent,
    NodeFinishEvent,
    IteratorProgressUpdateEvent,
]


# todo: FromUiNodeEvent-s


class EventQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def get(self) -> FromNodeEvent:
        return await self.queue.get()

    async def put(self, event: FromNodeEvent) -> None:
        await self.queue.put(event)
