import openai
import pymysql
import pandas as pd
import os

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput
from ...properties.outputs import TextOutput
from . import category as DatabaseCategory

from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI

template = """Act like you are a bartender. Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""


@NodeFactory.register("machines:image:summarizer")
class MySQLQueryNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Execute a SQL query on a MySQL database and return the data as a pandas DataFrame."
        self.inputs = [
            TextInput("OAI Secret"),
            TextInput("Question"),
            TextInput("SQL run result"),
        ]
        self.outputs = [TextOutput("Data Preview")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Result Summarizer"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, secret: str, question: str,
            sql_run_out: str) -> str:
        os.environ["OPENAI_API_KEY"] = secret
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who summarises the output of SQL execution in english."},
                {"role": "assistant", "content": f"the data output is: {sql_run_out} and the user's question was: {question}"},
                {"role": "assistant", "content": "Pretty print the output table then summarize to help the user with their question."}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

