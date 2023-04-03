from ...node_base import NodeBase
from ...node_factory import NodeFactory
import pandas as pd

from ...properties.inputs import TextInput
from . import category as DatabaseCategory
from ...properties.outputs.pandas_output import PandasOutput


@NodeFactory.register("machines:database:dataframe_rend")
class DataFrameExampleNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.inputs = [TextInput("html df"),]
        self.outputs = [PandasOutput(label="DataFrame")]
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
