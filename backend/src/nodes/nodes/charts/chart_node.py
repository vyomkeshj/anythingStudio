from typing import TypedDict, Any

from src.events import ToUIOutputMessage
from ...io.inputs import TextLineInput
from ...io.inputs.signal_input import SignalInput
from ...io.outputs import BaseOutput
from ...io.outputs.chart_output import ChartOutput
from ...io.rx.message_forwarder import ReactiveForwarder
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as ChartCategory

from aioreactive import AsyncSubject


class NewDatapoint(TypedDict):
    value: int
    label: str


class ChangeType(TypedDict):
    new_type: str


@NodeFactory.register("machines:chart:chart_node")
class ChartQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Generate live chart."
        self.chart_type = TextLineInput(label='Chart Type', default='pie2d')

        self.inputs = [
            SignalInput(label="Input Points"),
            self.chart_type,
        ]
        self.chart_output = ChartOutput()
        self.outputs = [self.chart_output]

        self.category = ChartCategory
        self.sub = "chart"
        self.name = "Live Chart"
        self.icon = "BsFillDatabaseFill"

        self.chart_type_name = 'line'

        self.consumer_subject = None
        self.subscriber = ReactiveForwarder(self.chart_output, 'new_datapoint')

        self.side_effects = True

    def run(self, signal: AsyncSubject, chart_type: str) -> str:
        self.consumer_subject = signal
        self.chart_type_name = chart_type
        return ''

    async def run_async(self):
        await send_ui_event('change_type', self.chart_output, ChangeType(new_type=self.chart_type_name))
        await self.consumer_subject.subscribe_async(self.subscriber)


async def send_ui_event(message_tag: str, output: BaseOutput, message: Any):
    channel_id = output.get_channel_id_by_name(message_tag)

    out_message = ToUIOutputMessage(channel_id=channel_id,
                                    data=message,
                                    message_tag=message_tag)
    await output.send_ui_event(event=out_message)
