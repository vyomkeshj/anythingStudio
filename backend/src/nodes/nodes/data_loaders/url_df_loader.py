from enum import Enum

import pandas as pd

from ...io.outputs.dataframe_output import DataframeOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as LoaderCategory


@NodeFactory.register("machines:loaders:dataframe_loader")
class UrlDfLoader(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Loads a df from url."
        self.inputs = [
            TextLineInput("Dataframe Url"),
        ]
        self.outputs = [DataframeOutput(label='Data')]

        self.category = LoaderCategory
        self.sub = "Pandas"
        self.name = "Dataframe [URL]"
        self.icon = "BsTable"

        self.side_effects = True
        self.schema = ""

    def run(self, dframe_url: str) -> pd.DataFrame:
        data = pd.read_csv(dframe_url)
        return data
