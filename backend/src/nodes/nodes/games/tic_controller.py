from reactivex.subject import Subject

from ...io.inputs import TextLineInput
from ...io.outputs.queue_output import SubjectOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.games import category as GamesCategory


@NodeFactory.register("machines:games:tic_controller")
class TicController(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "The computer controlling the tic tac toe."

        self.inputs = [TextLineInput(label="magic", default="life")]
        self.outputs = [SubjectOutput()]

        self.category = GamesCategory
        self.sub = "TicTacToe"
        self.name = "TicTacToe Controller"
        self.input_from_chatui_q: Subject = Subject()

        self.side_effects = True
        self.printer = lambda x: print(f"Echo From Controller Boi: {x}")

    def run(self, text: str) -> Subject:
        self.input_from_chatui_q.subscribe(lambda x: print(f"Echo From Controller Boi: {x}"))
        return self.input_from_chatui_q

    async def run_async(self):
        print("receiver ready 1")
        # while True:
        #     self.input_from_chatui_q.subscribe(lambda x: print(f"Echo From Controller Boi: {x}"))
