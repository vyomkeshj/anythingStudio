from ...node_base import NodeBase
from ...node_factory import NodeFactory
import pandas as pd

from ...io.inputs import TextInput
from . import category as DatabaseCategory
from ...io.outputs.html_outputs import HtmlOutput


@NodeFactory.register("machines:database:dataframe_rend")
class DataFrameExampleNode(NodeBase):

    # setup websocket connections with the ui node, setup the dataclasses as protocol, com channels
    def __init__(self):
        super().__init__()
        self.inputs = [TextInput("html df"),]
        self.outputs = [HtmlOutput(label="DataFrame")]
        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Show Dataframe"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, html: str) -> str:
        # data = {
        #     'Column1': [1, 2, 3, 4],
        #     'Column2': ['A', 'B', 'C', 'D'],
        # }
        # df = pd.DataFrame(data)
        return html
