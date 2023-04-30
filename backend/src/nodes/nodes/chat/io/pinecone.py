import chromadb.api.models.Collection

from src.nodes.io import expression
from src.nodes.io.inputs import BaseInput
from src.nodes.io.outputs import BaseOutput, OutputKind


class ChromaCollectionOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "AsyncSubject",
            kind: OutputKind = "generic",
    ):
        super().__init__(model_type, label, kind=kind, has_handle=True)


class ChromaCollectionInput(BaseInput):
    """Input for arbitrary text"""

    def __init__(
            self,
            label: str,
            has_handle=True,
    ):
        super().__init__(
            "string",
            label,
            has_handle=has_handle,
            kind="generic",
        )
        self.resizable = True

    def enforce(self, value) -> chromadb.api.models.Collection.Collection:
        if isinstance(value, chromadb.api.models.Collection.Collection):
            # stringify integers values
            return value
        else:
            raise ValueError(f"Expected a collection, got {value} of type {type(value)}")