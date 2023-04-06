from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import LargeImageOutput
from . import category as DatabaseCategory
import pandas as pd

class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


@NodeFactory.register("machines:database:plot_maker")
class HtmlPlotMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Plots a table."
        self.inputs = [
            TextInput("Data"),
            TextInput("Instructions"),
            TextInput("Hint"),
        ]
        self.outputs = [LargeImageOutput()]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Plot Maker"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, data: str, instruction: str, hint: str) -> str:
        table_data = pd.read_html(data)[0]

        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"{instruction}"},
                {"role": "system", "content": f"Dataframe Head: {table_data.head(2)}"},
                {"role": "user", "content": f"Hint: {hint}"}
            ]
        )
        resp = response['choices'][0]['message']['content'].strip()
        print(resp)
        return exec(resp)
