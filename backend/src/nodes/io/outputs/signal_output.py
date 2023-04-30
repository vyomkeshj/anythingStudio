from __future__ import annotations

from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class SignalOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "AsyncSubject",
            kind: OutputKind = "generic",
    ):
        super().__init__(model_type, label, kind=kind, has_handle=True)