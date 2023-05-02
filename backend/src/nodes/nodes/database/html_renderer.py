from ...node_base import NodeBase
from ...node_factory import NodeFactory

from ...io.inputs import TextInput
from . import category as DatabaseCategory
from ...io.outputs.html_outputs import HtmlOutput


@NodeFactory.register("machines:database:html_renderer")
class DataFrameExampleNode(NodeBase):

    # setup websocket connections with the ui node, setup the dataclasses as protocol, com channels
    def __init__(self):
        super().__init__()
        self.inputs = [TextInput("-> HTML In"),]
        self.outputs = [HtmlOutput(label="HTML Out ->")]
        self.category = DatabaseCategory
        self.sub = "Viewers"
        self.name = "Show HTML"

        self.side_effects = True

    def run(self, html: str) -> str:
        return html
