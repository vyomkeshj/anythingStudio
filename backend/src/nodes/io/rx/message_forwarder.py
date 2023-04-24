from typing import Any, Callable

from aioreactive import AsyncObserver
from sanic.log import logger

from src.events import ToUIOutputMessage
from src.nodes.io.outputs import BaseOutput


class ReactiveForwarder(AsyncObserver):

    def __init__(self, output: BaseOutput, channel_name: str, converter: Callable = None):
        super().__init__()
        self.output = output
        self.channel = channel_name

        self.converter = converter

    async def asend(self, value: Any) -> None:
        logger.info(f"Forwarding {value} to {self.channel}")
        if self.converter:
            value = await self.converter(value)
        await send_ui_event(self.channel, self.output, value)

    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")


async def send_ui_event(message_tag: str, output: BaseOutput, message: Any):
    channel_id = output.get_channel_id_by_name(message_tag)

    out_message = ToUIOutputMessage(channel_id=channel_id,
                                    data=message,
                                    message_tag=message_tag)
    await output.send_ui_event(event=out_message)
