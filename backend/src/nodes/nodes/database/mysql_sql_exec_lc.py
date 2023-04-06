import pymysql
import pandas as pd
import os

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextAreaInput, TextInput
from ...io.outputs import TextOutput
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


@NodeFactory.register("machines:image:run_sql_langchain")
class MySQLQueryNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Execute a SQL query on a MySQL database and return the data as a pandas DataFrame."
        self.inputs = [
            TextInput("OAI Secret"),
            TextInput("Agent Prompt"),
            TextInput("User Question"),

            TextInput("Host"),
            TextInput("User"),
            TextInput("Password"),
            TextInput("Database"),
            TextInput("SQL Query"),
        ]
        self.outputs = [TextOutput("Data Preview")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "Bartender <products table>"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, secret: str, prompt: str,
            question: str, host: str, user: str, password: str, database: str, sql_query: str) -> str:
        os.environ["OPENAI_API_KEY"] = secret

        print(f"host: {host}")
        connection = None
        try:
            connection = pymysql.connect(
                host=host,
                user=user,
                database=database,
                password=password,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected to MySQL server successfully.")
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                data = cursor.fetchall()

                dataframe = pd.DataFrame(data)
                agent = create_pandas_dataframe_agent(OpenAI(temperature=0),
                                         df = dataframe,
                                         verbose=True)
                out = agent.run(question)
                print(out)
                return str(out)
        except Exception as e:
            raise Exception(f"error: {e}")
        finally:
            if connection:
                connection.close()
