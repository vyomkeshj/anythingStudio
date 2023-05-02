from __future__ import annotations

from ...impl import clipboard
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import *
from ...io.outputs import *
from . import category as UtilityCategory


@NodeFactory.register("machines:utility:copy_to_clipboard")
class TextClipboardNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Copies the input to the clipboard."
        self.inputs = [
            ClipboardInput(),
        ]
        self.outputs = []

        self.category = UtilityCategory
        self.name = "Copy To Clipboard"
        self.sub = "Clipboard"

        self.side_effects = True

    def run(self, value: Union[str, np.ndarray]) -> None:
        if isinstance(value, np.ndarray):
            clipboard.copy_image(value)
        elif isinstance(value, str):  # type: ignore
            clipboard.copy_text(value)
        else:
            raise RuntimeError(f"Unsupported type {type(value)}")
