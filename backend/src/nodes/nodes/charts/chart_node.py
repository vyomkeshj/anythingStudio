from enum import Enum
from typing import TypedDict

from sanic.log import logger

from src.events import ToUIOutputMessage
from ...io.outputs.chart_output import ChartOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as ChartCategory

import asyncio


class MsgFromUser(TypedDict):
    msg: str


class MsgFromchartbot(TypedDict):
    msg: str


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
        pass
