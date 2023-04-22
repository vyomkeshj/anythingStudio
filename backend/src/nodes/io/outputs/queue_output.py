from .. import expression
from ...io.outputs.base_output import BaseOutput, OutputKind


class SubjectOutput(BaseOutput):
    def __init__(
            self,
            op_type: expression.ExpressionJson = "string",
            label: str = "Play",
            kind: OutputKind = "generic",
    ):
        super().__init__(output_type=op_type, label=label, kind=kind, has_handle=True)
