from langchain.agents import Tool
from langchain.utilities import PythonREPL

from ...nodes.chat.io.plugins import PluginOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.chat import category as ChatCategory


@NodeFactory.register("machines:langchain:python_repl")
class PythonReplTool(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain python repl tool."

        self.outputs = [PluginOutput(label="REPL Plugin ->", output_type="string")]

        self.category = ChatCategory
        self.sub = "Auto GPT Plugins"
        self.name = "Python Repl"

        self.side_effects = True

    def run(self, ) -> Tool:
        """Creates a list of tools from the inputs."""
        python_repl = PythonREPL()
        return Tool(
            name="Python REPL",
            func=python_repl.run,
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        )

    async def run_async(self):
        pass
