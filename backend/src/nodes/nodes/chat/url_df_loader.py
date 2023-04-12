from enum import Enum

import openai
import pandas as pd

from ...io.inputs.dataframe_input import DataframeInput
from ...io.outputs.dataframe_output import DataframeOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from ...io.outputs import ChatOutput, ImageOutput
from . import category as DatabaseCategory
import json as json_lib


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:database:dataframe_loader")
class UrlDfLoader(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Loads a df from url."
        self.inputs = [
            TextLineInput("Dataframe Url"),
        ]
        self.outputs = [DataframeOutput(label='Data')]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Dataframe Loader"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True
        self.schema = ""

    def run(self, dframe_url: str) -> pd.DataFrame:
        data = pd.read_csv(dframe_url)
        return data
