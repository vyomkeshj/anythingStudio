from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput, EnumInput, SliderInput
from ...properties.outputs import TextOutput, LargeImageOutput
from . import category as DatabaseCategory
from ...properties.outputs.pandas_output import HtmlOutput


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
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"{instruction}"},
                {"role": "system",
                 "content": f"Only respond with python code!"},

                {"role": "system", "content": f"Data: {data}"},
                {"role": "user", "content": f"Hint: {hint}"}
            ]
        )
        resp = response['choices'][0]['message']['content'].strip()
        print(resp)
        return exec(resp)
