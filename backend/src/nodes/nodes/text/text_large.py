from __future__ import annotations

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import TextOutput
from ..text import category as TextCategory


@NodeFactory.register("machines:text:text_large")
class TextValueNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Outputs the given text."
        self.inputs = [
            TextInput("Str:", min_length=0, kind="text"),
        ]
        self.outputs = [
            TextOutput("Str ->", output_type="Input0"),
        ]

        self.resizable = True
        self.side_effects: bool = True
        self.category = TextCategory
        self.name = "Large String"
        self.sub = "Value"


    def run(self, text: str) -> str:
        return text
