from __future__ import annotations

from enum import Enum

from src.nodes.node_base import NodeBase
from src.nodes.node_factory import NodeFactory
from src.nodes.properties.inputs import EnumInput, NumberInput, TextInput
from src.nodes.properties.outputs import TextOutput
from src.nodes.nodes.database import category as DatabaseCategory

class PaddingAlignment(Enum):
    START = "start"
    END = "end"
    CENTER = "center"


@NodeFactory.register("machines:database:text_padding")
class TextPaddingNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Pads text until it has a certain length."
        self.inputs = [
            TextInput("Text", min_length=0),
            NumberInput("Width", unit="chars"),
            TextInput(
                "Padding Character",
                has_handle=False,
                allow_numbers=False,
                min_length=1,
                max_length=1,
                placeholder="e.g. '0' or ' '",
            ),
            EnumInput(PaddingAlignment, label="Alignment"),
        ]
        self.outputs = [
            TextOutput(
                "Output Text",
                output_type="""
                match Input3 {
                    PaddingAlignment::Start => padStart(Input0, Input1, Input2),
                    PaddingAlignment::End => padEnd(Input0, Input1, Input2),
                    PaddingAlignment::Center => padCenter(Input0, Input1, Input2),
                }
                """,
            )
        ]

        self.category = DatabaseCategory
        self.name = "Text Padding"
        self.icon = "MdTextFields"
        self.sub = "Text"

    def run(
        self, text: str, width: int, padding: str, alignment: PaddingAlignment
    ) -> str:
        if alignment == PaddingAlignment.START:
            return text.rjust(width, padding)
        elif alignment == PaddingAlignment.END:
            return text.ljust(width, padding)
        elif alignment == PaddingAlignment.CENTER:
            return text.center(width, padding)
        else:
            raise ValueError(f"Invalid alignment '{alignment}'.")
