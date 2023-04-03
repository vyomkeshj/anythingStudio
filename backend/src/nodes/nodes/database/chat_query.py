from enum import Enum

import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput, EnumInput, SliderInput
from ...properties.outputs import TextOutput
from . import category as DatabaseCategory


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


@NodeFactory.register("machines:database:gpt4_sql")
class OpenAISQLMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "NL to sql."
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
        self.name = "gpt-4-sql"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, secret: str, schema: str, prompt: str, model_name: str, num_tokens: float, temp: float) -> str:
        openai.api_key = secret
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Given below are the table schemas for a MySQL database, use it to "
                                              "write a SQL query corresponding to the user's question, "
                                              "the table names are mentioned as [table_name] before each schema"},
                {"role": "system", "content": f"Schema: {schema}"},
                {"role": "system", "content": f"You only respond with correct SQL according to MySQL syntax and given columns and nothing else. Don't hallucinate new column names, use the ones from schema"},
                {"role": "user", "content": f"Question: {prompt}, SQL:"}
            ]
        )
        resp = response['choices'][0]['message']['content'].strip()
        print(resp)
        return resp