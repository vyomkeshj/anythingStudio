from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextAreaInput, TextInput, EnumInput, SliderInput
from ...io.outputs import TextOutput
from . import category as DatabaseCategory


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


@NodeFactory.register("machines:database:openai_api")
class OpenAISQLMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "NL to sql for insurance."
        self.inputs = [
            TextInput("Secret"),
            TextInput("Schema"),
            TextInput("Question"),
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
        self.outputs = [TextOutput("SQL")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "OAI SQL"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, secret: str, schema: str, prompt: str, model_name: str, num_tokens: float, temp: float) -> str:
        openai.api_key = secret
        prompt_init = f"""### Instruction: Given below is the database schema for MySQL database, use it to write a SQL query corresponding to the user's question, the table schemas are separated by ';'
        ### {schema}
        ### {prompt}
        ### SQL:"""
        print(prompt_init)

        response = openai.Completion.create(
            model=model_name,
            prompt=prompt_init,
            temperature=temp,
            max_tokens=round(num_tokens),
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
