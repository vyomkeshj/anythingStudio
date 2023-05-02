from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import  TextInput, SliderInput
from ...io.outputs import TextOutput
from . import category as ApiCategory


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


@NodeFactory.register("machines:api:gpt-api")
class OpenAISQLMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Hit GPT-x API with input."
        self.inputs = [
            TextInput("System Message"),
            TextInput("Prompt"),
            TextInput("ModelName", default="gpt-4"),
            SliderInput(
                "Completion Len",
                minimum=30,
                maximum=300,
                default=150,
                precision=1,
                controls_step=1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ],
            ),
            SliderInput(
                "Temperature",
                minimum=0,
                maximum=1,
                default=0.5,
                controls_step=0.1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ],
            ),
        ]
        self.outputs = [TextOutput("Out")]

        self.category = ApiCategory
        self.sub = "Dbase"
        self.name = "Openai API"


        self.side_effects = True

    def run(self, system_message: str, prompt: str, model_name: str, num_tokens: float, temp: float) -> str:
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": f"{system_message}"},
                {"role": "user", "content": f"Question: {prompt}"}
            ]
        )
        resp = response['choices'][0]['message']['content'].strip()
        return resp