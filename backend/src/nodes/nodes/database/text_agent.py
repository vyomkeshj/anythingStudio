import pymysql
import pandas as pd
import os

from langchain.chat_models import ChatOpenAI

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput
from ...properties.outputs import TextOutput
from . import category as DatabaseCategory
from langchain.prompts.prompt import PromptTemplate

from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from sqlalchemy import create_engine
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Use the following format:
        
        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"
        """


template = """Act like you are a bartender. Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""


@NodeFactory.register("machines:image:text_agent")
class MySQLQueryNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Execute a SQL query on a MySQL database and return the data as a pandas DataFrame."
        self.inputs = [
            TextInput("Agent Prompt"),
            TextInput("User Question"),
        ]
        self.outputs = [TextOutput("Response")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Sem Search"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, prompt: str, question: str) -> str:
        os.environ["OPENAI_API_KEY"] = "DsUoLtHg1IGhwvAgN78PT3BlbkFJpkBNvED6fl7lhjWtL1jB"

        try:
            db = SQLDatabase.from_uri("mysql+mysqlconnector://vyomkesh:$$5678Vyom!!@drinksmate.cbl2ralli4lr.ap-southeast-2.rds.amazonaws.com:3306/drinksmate")
            # llm = OpenAI(temperature=0, model_name="text-davinci-003")
            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
            db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
            answer = db_chain.run(question)
            print(answer)
            return str(answer)

        except Exception as error:
            return f"agh! {error}"


