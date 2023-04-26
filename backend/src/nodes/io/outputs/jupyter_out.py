from src.events import UIEvtChannelSchema
from .base_output import BaseOutput, OutputKind
from .. import expression


class JupyterOutput(BaseOutput):
    def __init__(
            self,
            model_type: expression.ExpressionJson = "string",
            label: str = "Notebook Viewer",
            kind: OutputKind = "jupyter",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='change_file',
                                          channel_direction='uplink',
                                          channel_id='')]

        super().__init__(model_type,label=label, channels=ui_channels, kind=kind)


    def get_broadcast_data(self, value: str):
        return value
