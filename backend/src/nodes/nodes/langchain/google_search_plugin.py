from langchain import SerpAPIWrapper
from langchain.agents import Tool

from .io.plugins import PluginOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.langchain import category as LangchainCategory


@NodeFactory.register("machines:langchain:serp_tool")
class PythonReplTool(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain google search repl plugin."

        self.outputs = [PluginOutput(label="Search Plugin ->", output_type="string")]

        self.category = LangchainCategory
        self.sub = "Plugins"
        self.name = "Google Search"

        self.side_effects = True

    def run(self, ) -> Tool:
        """Creates a list of tools from the inputs."""
        search = SerpAPIWrapper()
        return Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events",
        )

    async def run_async(self):
        pass
