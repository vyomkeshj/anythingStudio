from __future__ import annotations

from src.events import UIEvtChannelSchema
from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class AutoChartOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Natural language chart",
            kind: OutputKind = "auto_chart",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='submit_text',
                                          channel_direction='uplink',
                                          channel_id=''),
                       ]
        super().__init__(model_type, label, kind=kind, channels=ui_channels, has_handle=False)

