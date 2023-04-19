import asyncio
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union, TypeVar, Generic, Type

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


FromNodeEvent = Union[
    FinishEvent,
    ExecutionErrorEvent,
    NodeFinishEvent,
    IteratorProgressUpdateEvent,
]

# todo: this event is protobuf generated
SSE_Event = TypeVar('SSE_Event', bound=FromNodeEvent)


class EventChannel(Generic[SSE_Event]):
    def __init__(self, with_node: Optional[OutputId] = None):
        self.queue = asyncio.Queue()

    async def get(self) -> SSE_Event:
        return await self.queue.get()

    async def put(self, event: SSE_Event) -> None:
        await self.queue.put(event)


UIMessageType = TypeVar('UIMessageType', bound=TypedDict)


class ToUIOutputMessage(TypedDict):
    channel_id: str
    message_tag: str

    data: UIMessageType


class FromUIOutputMessage(TypedDict):
    channel_id: str
    message_tag: str

    data: UIMessageType


class UIEvtChannelKind(Enum):
    # messages to the ui
    UPLINK = "uplink"
    # messages from the ui
    DOWNLINK = "downlink"


class UIEvtChannelSchema(TypedDict):
    # Unique id for each channel, key for hashmap on ui that gets the event list. Set by the ui
    channel_id: Union[str, None]
    # The name of the channel is the tag for the message sent
    channel_name: str
    channel_direction: str


class UIEventChannel(EventChannel[Union[FromUIOutputMessage, ToUIOutputMessage]]):
    # All outputs have reference to an input and output channel to communicate with their ui
    def __init__(self, channel_name: str, kind: str):
        super().__init__()
        self.channel_name = channel_name
        self.kind = kind
        self.lock = asyncio.Lock()
        self.condition = asyncio.Condition(self.lock)

    async def get(self) -> Union[FromUIOutputMessage, ToUIOutputMessage]:
        """
            For the uplink channel
        """
        return await self.queue.get()

    async def get_message(self, channel_id: str) -> Union[FromUIOutputMessage, ToUIOutputMessage]:
        """
        awaits for a message with the specified channel_id.
        """
        async with self.condition:
            while True:
                # Look for a message with the specified channel_id
                for index, message in enumerate(self.queue._queue):
                    if message["channel_id"] == channel_id:
                        # Remove the message from the queue
                        del self.queue._queue[index]
                        return message

                # Wait for a new message to be added to the queue
                await self.condition.wait()

    async def put(self, event: Union[FromUIOutputMessage, ToUIOutputMessage]) -> None:
        async with self.condition:
            if self.kind == UIEvtChannelKind.DOWNLINK:
                if type(event) == FromUIOutputMessage:
                    raise IncorrectChannelError(self)
            elif self.kind == UIEvtChannelKind.UPLINK:
                if type(event) == ToUIOutputMessage:
                    raise IncorrectChannelError(self)

            await self.queue.put(event)
            self.condition.notify_all()

    def __str__(self):
        return f"{self.channel_name}, {self.kind})"


class IncorrectChannelError(Exception):
    """ If one tries to put a message to a downlink channel or get a message from an uplink channel"""

    def __init__(self, channel: UIEventChannel):
        self.channel = channel
        self.message = f"Trying to get from an uplink channel or put to a downlink channel: {channel}"

    def __str__(self):
        return self.message


class ChannelSetupError(Exception):
    """If one tries to use a channel without node_id and output_id set"""

    def __init__(self, channel: UIEventChannel):
        self.channel = channel
        self.message = f"Trying to use a channel without node_id and output_id set: {channel}"

    def __str__(self):
        return self.message
