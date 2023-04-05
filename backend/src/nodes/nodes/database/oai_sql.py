from enum import Enum

import openai

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor


from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput, EnumInput, SliderInput
from ...properties.outputs import TextOutput
from . import category as DatabaseCategory


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# @NodeFactory.register("machines:database:openai_api")
class OpenAISQLMaker(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "NL to sql for insurance."
        self.inputs = [
            TextInput("Secret"),
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
        self.outputs = [TextOutput("Completion")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Openai"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, secret: str, prompt: str, model_name: str, num_tokens: float, temp: float) -> str:
        openai.api_key = secret
        prompt_init = f"""### Instruction:
        Given below is the database schema for MySQL database, use it to write a SQL query corresponding to the user's question:
        ### insurance_claims (capital_gains, capital_loss, incident_date, incident_type, collision_type, incident_severity, authorities_contacted, incident_city, incident_location, incident_hour_of_the_day real, number_of_vehicles_involved, property_damage, bodily_injuries)
        ### {prompt}
        ### SQL:"""
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
