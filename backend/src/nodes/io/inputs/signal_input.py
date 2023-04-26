from .base_input import BaseInput
from ..expression import ExpressionJson
from aioreactive import AsyncSubject


class SignalInput(BaseInput):
    """Input for both ways com between nodes."""

    def __init__(
            self,
            label: str = "Signal",
            input_type: ExpressionJson = "string",
            has_handle: bool = True,
    ):
        super().__init__(input_type, label, has_handle=has_handle)

    def enforce(self, value):
        if AsyncSubject is not None:
            assert isinstance(value, AsyncSubject), "Expected a Async Subject."
        return value
