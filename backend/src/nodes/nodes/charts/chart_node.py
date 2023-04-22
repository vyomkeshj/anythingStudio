from enum import Enum
from typing import TypedDict
import random

from sanic.log import logger

from src.events import ToUIOutputMessage
from ...io.outputs.chart_output import ChartOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as ChartCategory

import asyncio


class NewDatapoint(TypedDict):
    value: int
    label: str


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chart:chart_node")
class ChartQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "chart with your database."
        self.inputs = [
            TextLineInput("ModelName", default="gpt-3.5-turbo")
        ]
        self.chart_output = ChartOutput()
        self.outputs = [self.chart_output]

        self.category = ChartCategory
        self.sub = "chart"
        self.name = "chartQ"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, use_model: str) -> str:
        """
            Initializes the chart node
        """

        return ''

    async def run_async(self):
        datapoint = int(random.uniform(1, 1000))
        await self.send_ui_event(NewDatapoint(value=datapoint, label=str(datapoint)))

        while True:
            await asyncio.sleep(5)
            datapoint = int(random.uniform(1, 1000))
            print(f"Sending new datapoint: {NewDatapoint(value=datapoint, label=str(datapoint))}")
            await self.send_ui_event(NewDatapoint(value=datapoint, label=str(datapoint)))

    async def send_ui_event(self, message: NewDatapoint):
        channel_id = self.chart_output.get_channel_id_by_name('new_datapoint')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="new_datapoint")
        await self.chart_output.send_ui_event(event=out_message)
