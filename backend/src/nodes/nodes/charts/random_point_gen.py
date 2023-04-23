from enum import Enum
from typing import TypedDict
import random

from aioreactive import AsyncSubject
from sanic.log import logger

from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import SliderInput
from . import category as ChartCategory
from async_signals import Signal

import asyncio


class NewDatapoint(TypedDict):
    value: int
    label: str


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chart:random_point_gen")
class RandomPointGen(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Generates Random Point For Chart."
        self.inputs = [
            SliderInput("Delay", default=3, minimum=1, maximum=10, slider_step=0.5),
        ]
        self.signal_output = SignalOutput(label="Random Points")
        self.outputs = [self.signal_output]

        self.category = ChartCategory
        self.sub = "Generators"
        self.name = "Point Generator"
        self.icon = "BsFillDatabaseFill"

        self.point_count = 0
        self.signal_src = AsyncSubject()
        self.delay = 2.5

        self.side_effects = True

    def run(self, delay: float) -> AsyncSubject:
        self.delay = delay
        return self.signal_src

    async def run_async(self):
        while True:
            self.point_count += 1
            await asyncio.sleep(self.delay)
            datapoint = int(random.uniform(1, 1000))
            await self.signal_src.asend(NewDatapoint(value=datapoint, label=str(datapoint)))

    async def send_ui_event(self, message: NewDatapoint):
        pass
