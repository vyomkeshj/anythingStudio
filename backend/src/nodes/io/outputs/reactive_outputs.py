from __future__ import annotations

from typing import TypedDict

from src.events import UIEvtChannelSchema
from src.nodes.io import expression
from src.nodes.io.outputs.base_output import BaseOutput, OutputKind


class SubmitText(TypedDict):
    submitted_text: str


class SubmittedResponse(TypedDict):
    successful: bool


class TextSenderOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Text Sender",
            kind: OutputKind = "text_sender",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='submit_text',
                                          channel_direction='downlink',
                                          channel_id=''),
                       UIEvtChannelSchema(channel_name='submit_response',
                                          channel_direction='uplink',
                                          channel_id='')]
        super().__init__(model_type, label, kind=kind, channels=ui_channels, has_handle=False)
