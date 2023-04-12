from .base_output import BaseOutput
from .. import expression
import pandas as pd


class DataframeOutput(BaseOutput):
    """Output for saving a local file"""

    def __init__(self, label: str, type: expression.ExpressionJson='any'):
        super().__init__(output_type=type, label=label)

    def validate(self, value) -> None:
        assert isinstance(value, pd.DataFrame)
