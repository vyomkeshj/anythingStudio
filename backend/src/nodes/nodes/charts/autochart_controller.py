import openai

from aioreactive import AsyncSubject, AsyncObserver
from sanic.log import logger

from ...io.inputs.signal_input import SignalInput
from ...io.outputs.auot_chart_output import ChartData
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from . import category as ChartCategory


@NodeFactory.register("machines:chart:controller")
class AutoChartController(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Takes in a user input and creates chart info for auto-chart node using openai API"
        self.inputs = [
            TextInput(label="Model", default="gpt-3.5-turbo", has_handle=False),
            SignalInput(label="Query"),
        ]
        self.outputs = [SignalOutput(label="[R] Chart Data ->")]

        self.category = ChartCategory
        self.sub = "Auto Chart"
        self.name = "Auto Chart Controller"


        self.side_effects = True
        self.consumer_subject = None
        self.output_subject = AsyncSubject()
        self.listener = None

    def run(self, model: str, subject: AsyncSubject) -> AsyncSubject:
        logger.info("subject is: " + str(subject))
        self.consumer_subject = subject
        self.listener = OpenAIListener(self.output_subject, model)

        return self.output_subject

    async def run_async(self):
        await self.consumer_subject.subscribe_async(self.listener)


class OpenAIListener(AsyncObserver):
    def __init__(self, send_to: AsyncSubject, model: str):
        super().__init__()
        self.output_subject = send_to
        self.model = model

    async def asend(self, value) -> None:
        logger.info("value is: " + str(value))
        input_val = value['submitted_text']
        chart_type = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": f"""The following are the possible chart types supported by the code provided: area, bar, line, composed, scatter, pie, radar, radialBar, treemap, and funnel. Given the user input: {input_val}, identify the chart type the user wants to display. Return just one word"""},
            ]
        )
        chart_type = chart_type['choices'][0]['message']['content'].strip()
        print("Chart type:", chart_type)

        chart_data = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""Generate a valid JSON in which each element is an object. Strictly using this FORMAT and naming: [{{"name": "a", "value": 12 }}] for the following description for Recharts. \n\n{input_val}\n;"""},
            ]
        )
        json = chart_data['choices'][0]['message']['content'].strip()
        data = ChartData(kind=chart_type, data=json)
        print("Chart data:", json)

        await self.output_subject.asend(data)

    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")
