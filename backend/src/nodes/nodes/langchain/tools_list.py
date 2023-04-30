from typing import Union, List

from langchain.agents import Tool

from .io.tools import ToolInput, ToolListOutput
from ...group import group
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.langchain import category as LangchainCategory

from ...utils.utils import ALPHABET


@NodeFactory.register("machines:langchain:tools_list")
class LangchainToolList(NodeBase):

    def __init__(self):
        super().__init__()
        self.description = "Creates a list of Langchain tools."

        self.inputs = [
            ToolInput("+A"),
            group("optional-list")(
                *[
                    ToolInput(f"+{letter}").make_optional()
                    for letter in ALPHABET[1:10]
                ],
            ),
        ]
        self.outputs = [ToolListOutput(label="Tools List ->")]

        self.category = LangchainCategory
        self.sub = "Tools"
        self.name = "Tools Provider"

        self.side_effects = True

    def run(self, *args: Union[Tool, None]) -> List[Union[Tool, None]]:
        """Creates a list of tools from the inputs."""
        inputs: List[Union[Tool, None]] = [*args]
        return [x for x in inputs if x is not None]

    async def run_async(self):
        pass
