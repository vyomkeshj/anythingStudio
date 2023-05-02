from langchain.agents import Tool, load_tools
from sanic.log import logger

from ...nodes.chat.io.plugins import PluginOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.chat import category as ChatCategory


@NodeFactory.register("machines:langchain:wolfram_plugin")
class WolframTool(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain wolfram alpha plugin."

        self.outputs = [PluginOutput(label="Wolfram Plugin ->", output_type="string")]

        self.category = ChatCategory
        self.sub = "Auto GPT Plugins"
        self.name = "Wolfram Alpha"

        self.side_effects = True

    def run(self, ) -> Tool:
        """Creates a wolfram tool."""

        tools = load_tools(["wolfram-alpha"])
        logger.info(f"Loaded wolfram: {len(tools)} tools.")
        return tools[0]
    async def run_async(self):
        pass
