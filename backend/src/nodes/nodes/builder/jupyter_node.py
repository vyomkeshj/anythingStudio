from typing import TypedDict, Any

from src.events import ToUIOutputMessage
from ...io.inputs import TextLineInput
from ...io.inputs.signal_input import SignalInput
from ...io.outputs import BaseOutput
from ...io.outputs.jupyter_out import JupyterOutput
from ...io.rx.message_forwarder import ReactiveForwarder
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as BuilderCategory

from aioreactive import AsyncSubject


@NodeFactory.register("machines:chart:jupyter")
class ChartQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Widget for displaying notebooks."

        self.inputs = [
            SignalInput(label="->", has_handle=False),
        ]
        self.jupyter_output = JupyterOutput()
        self.outputs = [self.jupyter_output]

        self.category = BuilderCategory
        self.sub = "jupyter"
        self.name = "Jupyter"
        self.icon = "BsFillDatabaseFill"

        self.chart_type_name = 'line'

        self.consumer_subject = None
        self.subscriber = ReactiveForwarder(self.jupyter_output, 'new_file')

        self.side_effects = True

    def run(self, signal: AsyncSubject, chart_type: str) -> str:
        self.consumer_subject = signal
        self.chart_type_name = chart_type
        return ''

    async def run_async(self):
        # await send_ui_event('new_file', self.jupyter_output, ChangeType(new_type=self.chart_type_name))
        await self.consumer_subject.subscribe_async(self.subscriber)


async def send_ui_event(message_tag: str, output: BaseOutput, message: Any):
    channel_id = output.get_channel_id_by_name(message_tag)

    out_message = ToUIOutputMessage(channel_id=channel_id,
                                    data=message,
                                    message_tag=message_tag)
    await output.send_ui_event(event=out_message)
