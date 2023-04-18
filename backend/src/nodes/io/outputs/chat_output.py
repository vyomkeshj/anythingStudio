from __future__ import annotations

import uuid

from src.events import ToUIOutputMessage, UIEvtChannelSchema, UIEvtChannelKind
from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class ChatOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Chat Viewer",
            kind: OutputKind = "chat",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='msg_from_chatbot',
                                          channel_direction='uplink',
                                          channel_id=str(uuid.uuid4())),
                       UIEvtChannelSchema(channel_name='msg_from_user',
                                          channel_direction='downlink',
                                          channel_id=str(uuid.uuid4()))]

        super().__init__(model_type, label, kind=kind, channels=ui_channels)

    def get_broadcast_data(self, value: str):
        return value

    async def send_ui_event(self, event: ToUIOutputMessage):
        await self.uplink_channel.put(event)
