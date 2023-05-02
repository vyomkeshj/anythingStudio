from typing import Tuple, List, Union

from aioreactive import AsyncSubject, AsyncObserver
from sanic.log import logger

from .impl.protocol import MsgHistoryItem, MsgFromUser, MsgFromChatbot
from ...io.inputs.signal_input import SignalInput
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as ChatCategory


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chat:chat_state")
class ChatState(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Connects to chat ui and maintains conversation state."
        self.inputs = [
            SignalInput(label="[R] next msg ->"),
            SignalInput(label="<- chat history [R]"),
        ]
        self.outputs = [SignalOutput(label="[R] bot msg out ->"), SignalOutput(label="<- usr msg in [R]")]

        self.category = ChatCategory
        self.sub = "ChatGPT"
        self.name = "Chat State"


        self.usr_msg_input: AsyncSubject = AsyncSubject()  # type: ignore
        self.next_msg_output: AsyncSubject = AsyncSubject()  # type: ignore

        self.bot_nxt_msg_in: AsyncSubject = AsyncSubject()  # type: ignore
        self.history_out: AsyncSubject = AsyncSubject()  # type: ignore

        self.bot_nxt_msg_in_sub = None
        self.usr_msg_input_sub = None

        self.msg_history: List[MsgHistoryItem] = []

        self.info = "Stores the state of the chat box."

        self.side_effects = True
        self.msg_observer = None

    def run(self, bot_nxt_msg_in: AsyncSubject, history_out: AsyncSubject) -> Tuple[AsyncSubject, AsyncSubject]:
        """
            Initializes the controller
        """
        self.bot_nxt_msg_in = bot_nxt_msg_in
        self.history_out = history_out

        return self.next_msg_output, self.usr_msg_input

    async def run_async(self):
        if self.msg_observer is None:
            self.msg_observer = MessageObserver(self)
        if self.bot_nxt_msg_in_sub is None:
            self.bot_nxt_msg_in_sub = await self.bot_nxt_msg_in.subscribe_async(self.msg_observer)
        if self.usr_msg_input_sub is None:
            self.usr_msg_input_sub = await self.usr_msg_input.subscribe_async(self.msg_observer)


class MessageObserver(AsyncObserver):

    def __init__(self, state_node: ChatState):
        super().__init__()
        self.state_node: ChatState = state_node

    async def asend(self, input_msg: Tuple[str, Union[MsgFromUser, MsgFromChatbot]]) -> None:
        if input_msg[0] == "msg_from_user":
            # add received message to history
            self.state_node.msg_history.append(MsgHistoryItem(role="user", content=input_msg[1]["msg"]))
            # send history to history_out
            await self.state_node.history_out.asend(self.state_node.msg_history)

        elif input_msg[0] == "msg_from_chatbot":
            message = input_msg[1]
            self.state_node.msg_history.append(MsgHistoryItem(role="assistant", content=message["msg"]))
            await self.state_node.next_msg_output.asend(message)
        else:
            logger.error(f"Received {input_msg} in state node from unknown source")

    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")
