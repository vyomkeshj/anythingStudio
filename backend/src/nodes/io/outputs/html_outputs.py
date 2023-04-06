import pandas as pd
from .base_output import BaseOutput, OutputKind
from .. import expression


class HtmlOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Dataframe Viewer",
            kind: OutputKind = "html",
    ):
        super().__init__(model_type, label, kind=kind)

    def get_broadcast_data(self, value: str):
        return value
