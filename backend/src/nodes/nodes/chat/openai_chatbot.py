from typing import Tuple, List

from aioreactive import AsyncSubject, AsyncObserver
from openai_async import openai_async

from .impl.protocol import MsgHistoryItem, MsgFromChatbot
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import SliderInput, TextInput
from . import category as ChatCategory


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chat:oai_chatbot")
class OAIChatbot(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Connects to chat ui and maintains conversation state."
        self.inputs = [
            TextInput(label="System Message"),
            SliderInput(
                "Completion Len",
                minimum=30,
                maximum=300,
                default=30,
                precision=1,
                controls_step=1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ]),
        ]
        self.outputs = [SignalOutput(label="history in <-"), SignalOutput(label="next msg out ->")]

        self.category = ChatCategory
        self.sub = "Chatbots"
        self.name = "OpenAI Chatbot"
        self.icon = "BsFillDatabaseFill"

        self.history_input: AsyncSubject = AsyncSubject()     # type: ignore
        self.nxt_msg_op: AsyncSubject = AsyncSubject()    # type: ignore
        self.completion_len = 150
        self.controller = None

        self.api_key = None
        self.system_message: str = ''   # type: ignore

        self.info = "Stores the state of the chat box."
        self.controller = StateObserver(self)

        self.side_effects = True

    def run(self, system_message: str, completion_len: int) -> Tuple[AsyncSubject, AsyncSubject]:
        """
            Initializes the controller
        """
        self.completion_len = completion_len
        self.api_key = "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"
        self.system_message = system_message

        return self.history_input, self.nxt_msg_op

    async def run_async(self):
        await self.history_input.subscribe_async(self.controller)


class StateObserver(AsyncObserver):

    def __init__(self, state_node: OAIChatbot):
        super().__init__()
        self.state_node: OAIChatbot = state_node

    async def asend(self, input_hist: List[MsgHistoryItem]) -> None:
        input_hist.insert(0, {"role": "system", "content": self.state_node.system_message})

        response = await openai_async.chat_complete(
            self.state_node.api_key,
            timeout=5,
            payload={
                "model": "gpt-3.5-turbo",
                "messages": input_hist,
                "max_tokens": self.state_node.completion_len,
            },

        )
        if "choices" in response.json():
            msg_from_chatbot = response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception("No choices in response")

        await self.state_node.nxt_msg_op.asend(("msg_from_chatbot", MsgFromChatbot(msg=msg_from_chatbot)))

    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")
