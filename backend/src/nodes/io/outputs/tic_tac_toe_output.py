from src.events import UIEvtChannelSchema
from .. import expression
from ...io.outputs.base_output import BaseOutput, OutputKind


class TicTacToeOutput(BaseOutput):
    def __init__(
            self,
            op_type: expression.ExpressionJson = "string",
            label: str = "Play",
            kind: OutputKind = "tic_tac_toe",
    ):
        ui_channels = [UIEvtChannelSchema(channel_name='move_from_computer',
                                          channel_direction='uplink',
                                          channel_id=''),
                       UIEvtChannelSchema(channel_name='move_from_user',
                                          channel_direction='downlink',
                                          channel_id='')]

        super().__init__(output_type=op_type, label=label, kind=kind, channels=ui_channels, has_handle=False)
