from __future__ import annotations

import uuid

from src.events import ToUIOutputMessage, UIEvtChannelSchema, UIEvtChannelKind
from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class ChartOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Chart Viewer",
            kind: OutputKind = "chart",
    ):
        super().__init__(model_type, label, kind=kind, has_handle=False)
