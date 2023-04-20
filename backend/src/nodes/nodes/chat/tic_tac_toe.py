from typing import TypedDict

from src.events import ToUIOutputMessage
from ...io.outputs.tic_tac_toe_output import TicTacToeOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as ChatCategory


class MoveFromUser(TypedDict):
    row: int
    col: int


class MoveFromComputer(TypedDict):
    row: int
    col: int


@NodeFactory.register("machines:database:tic_tac_toe")
class TicTacToeNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Play Tic Tac Toe against the computer."

        self.tic_tac_toe_output = TicTacToeOutput()
        self.outputs = [self.tic_tac_toe_output]

        self.category = ChatCategory
        self.sub = "TicTacToe"
        self.name = "TicTacToe"
        self.icon = "MdOutlineColorLens"

        self.side_effects = True

    def run(self) -> str:
        """Initialize the tic tac toe node"""
        return ''

    async def run_async(self):
        # Implement the game logic here
        pass

    async def send_ui_event(self, message: MoveFromComputer):
        channel_id = self.tic_tac_toe_output.get_channel_id_by_name('move_from_computer')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="move_from_computer")
        await self.tic_tac_toe_output.send_ui_event(event=out_message)

    async def receive_ui_event(self) -> MoveFromUser:
        event = await self.tic_tac_toe_output.receive_ui_event(channel_name='move_from_user')
        return event['data']
