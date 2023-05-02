from __future__ import annotations

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import MarkdownOutput

from ...nodes.database import category as DatabaseCategory


@NodeFactory.register("machines:text:markdown")
class MarkdownRendererNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Outputs the given text."
        self.inputs = [
            TextInput("Markdown Response ->", min_length=0),
        ]
        self.outputs = [
            MarkdownOutput(),
        ]

        self.resizable = True
        self.side_effects: bool = True
        self.category = DatabaseCategory
        self.sub = "Viewers"
        self.name = "Markdown Viewer"

    def run(self, text: str) -> str:
        return text
