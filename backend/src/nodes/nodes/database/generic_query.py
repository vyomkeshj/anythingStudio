from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextAreaInput, TextInput, EnumInput, SliderInput
from ...io.outputs import TextOutput
from . import category as DatabaseCategory

from reactivex import create

class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


@NodeFactory.register("machines:database:gpt4_generic")
class OpenAISQLMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Generic tasks using gpt4 prompts."
        self.inputs = [
            TextInput("System Message"),
            TextInput("Prompt"),
            TextInput("ModelName"),
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
                default=0,
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

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Gpt task"
        self.icon = "BsFillDatabaseFill"

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