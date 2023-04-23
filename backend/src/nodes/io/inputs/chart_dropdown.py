from enum import Enum

from ...impl.image_utils import BorderType
from .generic_inputs import DropDownInput, EnumInput


class ChartType(Enum):
    PIE2D = 0,
    LINE = 1




def ChartTypeInput() -> DropDownInput:
    return EnumInput(
        ChartType,
        default_value=ChartType.LINE,
        option_labels={
            ChartType.LINE: "line",
            ChartType.PIE2D: "pie2d",
        },
        # extra_definitions="""
        #     def BorderType::getOutputChannels(type: BorderType, channels: uint) {
        #         match type {
        #             BorderType::Transparent => 4,
        #             _ => channels
        #         }
        #     }
        # """,
    )
