from __future__ import annotations

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import NumberOutput

from ..text import category as TextCategory


@NodeFactory.register("machines:text:text_length")
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

        self.category = TextCategory
        self.name = "Text Length"
        self.sub = "Text"

    def run(self, text: str) -> int:
        return len(text)
