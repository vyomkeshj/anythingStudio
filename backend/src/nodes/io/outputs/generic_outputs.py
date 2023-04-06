from __future__ import annotations

from ...utils.seed import Seed
from .. import expression
from .base_output import BaseOutput, OutputKind


class NumberOutput(BaseOutput):
    def __init__(
            self,
            label: str,
            output_type: expression.ExpressionJson = "number",
    ):
        super().__init__(expression.intersect("number", output_type), label)

    def get_broadcast_type(self, value: int | float):
        return expression.literal(value)

    def validate(self, value) -> None:
        assert isinstance(value, (int, float))


class MarkdownOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Markdown Viewer",
            kind: OutputKind = "markdown",
    ):
        super().__init__(model_type, label, kind=kind)

    def get_broadcast_data(self, value: str):
        return value

class ChatOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Chat Viewer",
            kind: OutputKind = "chat",
    ):
        super().__init__(model_type, label, kind=kind)

    def get_broadcast_data(self, value: str):
        return value


class TextOutput(BaseOutput):
    def __init__(
            self,
            label: str,
            output_type: expression.ExpressionJson = "string",
    ):
        super().__init__(expression.intersect("string", output_type), label)

    def get_broadcast_type(self, value: str):
        return expression.literal(value)

    def validate(self, value) -> None:
        assert isinstance(value, str)


def FileNameOutput(label: str = "Name", of_input: int | None = None):
    output_type = (
        "string"
        if of_input is None
        else f"splitFilePath(Input{of_input}.path).basename"
    )

    return TextOutput(label=label, output_type=output_type)


class SeedOutput(BaseOutput):
    def __init__(self, label: str = "Seed"):
        super().__init__(output_type="Seed", label=label, kind="generic")

    def validate(self, value) -> None:
        assert isinstance(value, Seed)
