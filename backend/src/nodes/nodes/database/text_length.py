from __future__ import annotations

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import NumberOutput

from . import category as DatabaseCategory


@NodeFactory.register("machines:database:text_length")
class TextLengthNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Returns the number characters in a string of text."
        self.inputs = [
            TextInput("Text", min_length=0),
        ]
        self.outputs = [
            NumberOutput("Length", output_type="string::len(Input0)"),
        ]

        self.category = DatabaseCategory
        self.name = "Text Length"
        self.icon = "MdTextFields"
        self.sub = "Text"

    def run(self, text: str) -> int:
        return len(text)
