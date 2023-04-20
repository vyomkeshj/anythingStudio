from asyncio import Queue

from .base_input import BaseInput
from ..expression import ExpressionJson


class QueueInput(BaseInput):
    """Input for both ways com between nodes."""

    def __init__(
            self,
            label: str = "Queue",
            input_type: ExpressionJson = "string",
    ):
        super().__init__(input_type, label)

    def enforce(self, value):
        if Queue is not None:
            assert isinstance(value, Queue), "Expected an async io queue."
        return value

