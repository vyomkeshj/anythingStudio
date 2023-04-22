from .base_input import BaseInput
from ..expression import ExpressionJson
from reactivex.subject import Subject


class SubjectInput(BaseInput):
    """Input for both ways com between nodes."""

    def __init__(
            self,
            label: str = "Queue",
            input_type: ExpressionJson = "string",
    ):
        super().__init__(input_type, label)

    def enforce(self, value):
        if Subject is not None:
            assert isinstance(value, Subject), "Expected a Subject."
        return value

