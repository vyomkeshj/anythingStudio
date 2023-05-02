from sanic.log import logger

from ...io.inputs.signal_input import SignalInput
from ...io.outputs.auot_chart_output import AutoChartOutput
from ...io.rx.message_forwarder import ReactiveForwarder
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as ChartCategory
from aioreactive import AsyncSubject


@NodeFactory.register("machines:chart:autochart")
class AutoChartComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Generate chart from text."

        self.inputs = [
            SignalInput(label="-> Chart Data [R]"),
        ]
        self.chart_output = AutoChartOutput()
        self.outputs = [self.chart_output]

        self.category = ChartCategory
        self.sub = "Auto Chart"
        self.name = "Auto Chart Viewer"

        self.consumer_subject = None
        self.subscriber = ReactiveForwarder(self.chart_output, 'chart_data')

        self.side_effects = True

    def run(self, subject: AsyncSubject) -> str:
        self.consumer_subject = subject
        return ''

    async def run_async(self):
        await self.consumer_subject.subscribe_async(self.subscriber)




