import pandas as pd

from .base_input import BaseInput
from ..expression import ExpressionJson


class DataframeInput(BaseInput):
    """Input a loaded model"""

    def __init__(
            self,
            label: str = "Dataframe",
            input_type: ExpressionJson = "string",
    ):
        super().__init__(input_type, label)

    def enforce(self, value):
        if pd is not None:
            assert isinstance(value, pd.DataFrame), "Expected a Pandas Dataframe."
        return value

