from langchain.agents import Tool
from sanic.log import logger

from src.nodes.nodes.chat.io.plugins import PluginOutput
from src.nodes.node_base import NodeBase
from src.nodes.node_factory import NodeFactory
from src.nodes.nodes.chat import category as ChatCategory
from langchain.agents import load_tools


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
