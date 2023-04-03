import pymysql
import pandas as pd

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import TextAreaInput, TextInput
from ...properties.outputs import TextOutput
from . import category as DatabaseCategory


@NodeFactory.register("machines:image:run_sql")
class MySQLQueryNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Execute a SQL query on a MySQL database and return the data as a pandas DataFrame."
        self.inputs = [
            TextInput("Host"),
            TextInput("User"),
            TextInput("Password"),
            TextInput("Database"),
            TextInput("SQL Query"),
        ]
        self.outputs = [TextOutput("Data Preview")]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "MySQL Query"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, host: str, user: str, password: str, database: str, sql_query: str) -> str:
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
                return pd.DataFrame(data).to_html()

        except Exception as e:
            raise Exception(f"error: {e}")
        finally:
            if connection:
                connection.close()
