from __future__ import annotations

from typing import Union

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextAreaInput
from . import category as UtilityCategory


@NodeFactory.register("machines:utility:note")
class NoteNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Sticky Note."
        self.inputs = [
            TextAreaInput(label="Note Text").make_optional(),
        ]
        self.outputs = []

        self.category = UtilityCategory
        self.name = "Note"
        self.sub = "Text"

    def run(self, _text: Union[str, None]) -> None:
        return
