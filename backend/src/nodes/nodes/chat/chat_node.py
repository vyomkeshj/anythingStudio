from enum import Enum
from typing import TypedDict

from sanic.log import logger

from src.events import ToUIOutputMessage
from ...io.outputs.chat_output import ChatOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as ChatCategory

import asyncio


class MsgFromUser(TypedDict):
    msg: str


class MsgFromChatbot(TypedDict):
    msg: str


class Models(Enum):
    GPT3 = "text-davinci-003"
    GPT35 = "gpt-3.5-turbo"


# some way to just tag this as websocket node?
@NodeFactory.register("machines:database:chat_node")
class ChatQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Chat with your database."
        self.inputs = [
            TextLineInput("ModelName", default="gpt-3.5-turbo")
        ]
        self.chat_output = ChatOutput()
        self.outputs = [self.chat_output]

        self.category = ChatCategory
        self.sub = "Dbase"
        self.name = "ChatQ"
        self.icon = "BsFillDatabaseFill"

        self.side_effects = True

    def run(self, use_model: str) -> str:
        """
            Initializes the chat node
        """

        return ''

    async def run_async(self):
        await self.send_ui_event(MsgFromChatbot(msg="gonna say what you say 5 sec later"))

        while True:
            received = await self.receive_ui_event()
            if received['msg'] == 'quit':
                break
            await asyncio.sleep(5)
            await self.send_ui_event(MsgFromChatbot(msg=f"Echo: {received['msg']}"))

    async def send_ui_event(self, message: MsgFromChatbot):
        channel_id = self.chat_output.get_channel_id_by_name('msg_from_chatbot')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="msg_from_chatbot")
        await self.chat_output.send_ui_event(event=out_message)

    async def receive_ui_event(self) -> MsgFromUser:
        event = await self.chat_output.receive_ui_event(channel_name='msg_from_user')
        return event['data']
