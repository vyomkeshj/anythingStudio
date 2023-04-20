import asyncio
from typing import TypedDict

from .tic_tac_toe import MoveFromUser
from ...io.inputs import TextLineInput
from ...io.outputs.queue_output import QueueOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as ChatCategory


@NodeFactory.register("machines:database:tic_controller")
class TicController(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "The computer controlling the tic tac toe."

        self.inputs = [TextLineInput(label="magic", default="life")]
        self.outputs = [QueueOutput()]

        self.category = ChatCategory
        self.sub = "TicTacToe"
        self.name = "TicTacToe Controller"
        self.icon = "MdOutlineColorLens"
        self.input_from_chatui_q = asyncio.Queue()

        self.side_effects = True

    def run(self, text: str) -> asyncio.Queue:
        return self.input_from_chatui_q

    async def run_async(self):
        print("receiver ready 1")
        # while True:
        #     print("receiver ready")
        #     received: MoveFromUser = await self.input_from_chatui_q.get()
        #     print(f"Echo From Controller Boi: {received}")
