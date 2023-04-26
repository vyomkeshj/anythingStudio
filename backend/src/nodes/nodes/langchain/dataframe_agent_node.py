import asyncio
from typing import TypedDict

from src.events import ToUIOutputMessage
from ...io.inputs.queue_input import SubjectInput
from ...io.outputs.tic_tac_toe_output import TicTacToeOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.langchain import category as LangchainCategory

from reactivex.subject import Subject


class MoveFromUser(TypedDict):
    row: int
    col: int


class MoveFromComputer(TypedDict):
    row: int
    col: int


@NodeFactory.register("machines:langchain:df_agent")
class TicTacToeNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain git loader."

        self.tic_tac_toe_output = TicTacToeOutput()
        # self.inputs = [SubjectInput(label="controller")]
        self.outputs = [self.tic_tac_toe_output]

        self.category = LangchainCategory
        self.sub = "Loaders"
        self.name = "GitLoader"
        # self.icon = "MdOutlineColorLens"
        self.controller: Subject = None    # type: ignore

        self.side_effects = True

    def run(self) -> str:
        """Initialize the tic tac toe node"""
        # self.controller = input_controller
        # kb_loader = GitLoader(
        #     clone_url="https://github.com/neo4j-documentation/knowledge-base",
        #     repo_path="./repos/kb/",
        #     branch="master",
        #     file_filter=lambda file_path: file_path.endswith(".adoc")
        #                                   and "articles" in file_path,
        # )

        return ''

    async def run_async(self):
        print("running async in tic tac toe node")
        while True:
            received: MoveFromUser = await self.receive_ui_event()
            print(f"Echo: {received}")

            # self.controller.on_next(received)

    async def send_ui_event(self, message: MoveFromComputer):
        channel_id = self.tic_tac_toe_output.get_channel_id_by_name('move_from_computer')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="move_from_computer")
        await self.tic_tac_toe_output.send_ui_event(event=out_message)

    async def receive_ui_event(self) -> MoveFromUser:
        event = await self.tic_tac_toe_output.receive_ui_event(channel_name='move_from_user')
        return event['data']
