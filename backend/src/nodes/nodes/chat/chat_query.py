from enum import Enum

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from ...io.outputs import ChatOutput
from . import category as DatabaseCategory
import json as json_lib


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:database:chat_node")
class ChatQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Chat with your database."
        self.inputs = [
            TextLineInput("Schema"),
            TextLineInput("ModelName", default="gpt-3.5-turbo")
        ]
        self.outputs = [ChatOutput(label='ChatQ')]

        self.category = DatabaseCategory
        self.sub = "Dbase"
        self.name = "ChatQ"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True
        self.schema = ""

    def run(self, prompt: str, use_model: str) -> str:
        """Run runs only once so we can use it to initialize the machine
        Return json in format: { database_schema: string; use_model: string;}
        """
        return json_lib.dumps({"database_schema": prompt, "use_model": use_model})

