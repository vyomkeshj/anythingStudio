from typing import Union, List

from langchain.agents import Tool

from src.nodes.nodes.chat.io.plugins import PluginInput, PluginListOutput
from src.nodes.group import group
from src.nodes.node_base import NodeBase
from src.nodes.node_factory import NodeFactory
from src.nodes.nodes.chat import category as ChatCategory

from src.nodes.utils.utils import ALPHABET


@NodeFactory.register("machines:langchain:plugins_list")
class LangchainToolList(NodeBase):

    def __init__(self):
        super().__init__()
        self.description = "Creates a list of Langchain tools."

        self.inputs = [
            PluginInput("+TODO Plugin"),
            group("optional-list")(
                *[
                    PluginInput(f"+Plugin {letter}").make_optional()
                    for letter in ALPHABET[1:10]
                ],
            ),
        ]
        self.outputs = [PluginListOutput(label="Plugins List ->")]

        self.category = ChatCategory
        self.sub = "Auto GPT Plugins"
        self.name = "Plugins Provider"

        self.side_effects = True

    def run(self, *args: Union[Tool, None]) -> List[Union[Tool, None]]:
        """Creates a list of tools from the inputs."""
        inputs: List[Union[Tool, None]] = [*args]
        return [x for x in inputs if x is not None]

    async def run_async(self):
        pass
