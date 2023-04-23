from __future__ import annotations

import uuid

from src.events import ToUIOutputMessage, UIEvtChannelSchema, UIEvtChannelKind
from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class ChartOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Chart Viewer",
            kind: OutputKind = "chart",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='new_datapoint',
                                          channel_direction='uplink',
                                          channel_id=''),
                       UIEvtChannelSchema(channel_name='change_type',
                                          channel_direction='uplink',
                                          channel_id='')]
        super().__init__(model_type, label, kind=kind, channels=ui_channels, has_handle=False)

    async def send_ui_event(self, event: ToUIOutputMessage):
        await self.uplink_channel.put(event)
