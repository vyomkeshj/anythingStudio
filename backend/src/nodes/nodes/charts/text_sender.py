from __future__ import annotations

import asyncio
from typing import Tuple

from aioreactive import AsyncSubject

from ...io.inputs import SliderInput
from ...io.outputs.reactive_outputs import TextSenderOutput
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.charts import category as ChartCategory


@NodeFactory.register("machines:chart:text_sender")
class TextSenderNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Sends the Query to the connected nodes reactively."
        self.signal_output = SignalOutput(label="[R] Query ->")
        self.inputs = [
            SliderInput("Debounce", default=2, minimum=1, maximum=10, slider_step=0.5),
        ]
        self.text_sender_output = TextSenderOutput()
        self.outputs = [
            self.text_sender_output,
            self.signal_output,
        ]

        self.resizable = True
        self.side_effects: bool = True
        self.category = ChartCategory
        self.name = "Query Sender"
        self.sub = "Reactive Inputs"
        self.signal_src = AsyncSubject()
        self.delay = 0.1

    def run(self, delay: float) -> Tuple[str, AsyncSubject]:
        # fixme: every node must have at least one input, why???
        # self.delay = delay
        # Belay the delay
        return '', self.signal_src

    async def run_async(self):
        while True:
            event = await self.text_sender_output.receive_ui_event(channel_name='submit_text')
            await asyncio.sleep(self.delay)
            await self.signal_src.asend(event['data'])
            # todo: send response
