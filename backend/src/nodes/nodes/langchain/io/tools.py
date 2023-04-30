from typing import List

from langchain.agents import Tool

from src.nodes.io import expression
from src.nodes.io.expression import ExpressionJson
from src.nodes.io.inputs import BaseInput
from src.nodes.io.outputs import BaseOutput, OutputKind


class ToolInput(BaseInput):
    """Langchain Tool as Input."""

    def __init__(
            self,
            label: str = "Tool",
            input_type: ExpressionJson = "string",
    ):
        super().__init__(input_type, label)

    def enforce(self, value):
        if Tool is not None:
            assert isinstance(value, Tool), "Expected a Langchain tool."
        return value


class ToolListInput(BaseInput):
    """Langchain Tools list as Input."""

    def __init__(
            self,
            label: str = "Tools List ->",
            input_type: ExpressionJson = "string",
    ):
        super().__init__(input_type, label)

    def enforce(self, value):
        if List is not None:
            assert isinstance(value, List), "Expected a list of Langchain tools."
        return value


class ToolListOutput(BaseOutput):
    """Output list of Langchain tools"""

    def __init__(
            self,
            label: str,
            output_type: expression.ExpressionJson = "string",
            kind: OutputKind = "generic",
            has_handle: bool = True,
    ):
        super().__init__(output_type, label, kind=kind, has_handle=has_handle)

    def validate(self, value) -> None:
        assert isinstance(value, List)


class ToolOutput(BaseOutput):
    """Output a Langchain tool"""

    def __init__(
            self,
            output_type: expression.ExpressionJson,
            label: str,
            kind: OutputKind = "generic",
            has_handle: bool = True,
    ):
        super().__init__(output_type, label, kind=kind, has_handle=has_handle)

    def validate(self, value) -> None:
        assert isinstance(value, Tool)
