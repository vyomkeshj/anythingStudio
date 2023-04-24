from sanic.log import logger

from ...io.inputs.signal_input import SignalInput
from ...io.outputs.auo_chart_output import AutoChartOutput
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
            SignalInput(label="Info Input"),
        ]
        self.chart_output = AutoChartOutput()
        self.outputs = [self.chart_output]

        self.category = ChartCategory
        self.sub = "chart"
        self.name = "Auto Chart"
        self.icon = "BsFillDatabaseFill"
        self.consumer_subject = None
        self.subscriber = ReactiveForwarder(self.chart_output, 'submit_text')

        self.side_effects = True

    def run(self, subject: AsyncSubject) -> str:
        self.consumer_subject = subject
        return ''

    async def run_async(self):
        # fixme: hit the openai api here?
        await self.consumer_subject.subscribe_async(self.subscriber)




