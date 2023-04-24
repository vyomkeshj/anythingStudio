from typing import Any

from aioreactive import AsyncObserver
from sanic.log import logger

from src.events import ToUIOutputMessage
from src.nodes.io.outputs import BaseOutput


class ReactiveForwarder(AsyncObserver):

    def __init__(self, output: BaseOutput, channel_name: str):
        super().__init__()
        self.output = output
        self.channel = channel_name

    async def asend(self, value: Any) -> None:
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
