from typing import TypedDict

from src.events import UIEvtChannelSchema
from src.nodes.io.outputs import BaseOutput


class CodeInput(TypedDict):
    code: str

class CodeOutput(BaseOutput):
    def __init__(self):
        super().__init__(
            output_type="string",
            label="Code Output",
            kind="generic",
            has_handle=False,
            channels=[
                UIEvtChannelSchema(channel_name="submit_text", channel_direction="downlink", channel_id=""),
                UIEvtChannelSchema(channel_name="submit_response", channel_direction="uplink", channel_id=""),
            ],
        )

