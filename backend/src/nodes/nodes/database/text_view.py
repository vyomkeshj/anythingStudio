from __future__ import annotations

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import TextOutput
from . import category as DatabaseCategory


@NodeFactory.register("machines:database:text_view")
class TextValueNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Shows."
        self.inputs = [
            TextInput("Text", min_length=300, has_handle=True),
        ]
        self.outputs = [
            TextOutput("Output", output_type='Input0'),
        ]

        self.resizable = True
        self.side_effects: bool = True
        self.category = DatabaseCategory
        self.name = "ErrorPopup"
        self.icon = "MdTextFields"
        self.sub = "Value"

    def run(self, text: str) -> None:
        return str
