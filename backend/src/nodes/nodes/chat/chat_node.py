import asyncio

from aioreactive import AsyncSubject
from sanic.log import logger

from src.events import ToUIOutputMessage
from src.nodes.nodes.chat.impl.protocol import MsgFromChatbot, MsgFromUser
from ...io.inputs.signal_input import SignalInput
from ...io.outputs.chat_output import ChatOutput
from ...io.rx.message_forwarder import ReactiveForwarder
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextLineInput
from . import category as ChatCategory


@NodeFactory.register("machines:chat:chat_node")
class ChatQComponent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Chat with chatgpt."
        self.inputs = [
            TextLineInput(label="<i>"),
            SignalInput(label="-> chatbot msg in [R]"),
            SignalInput(label="<- usr msg out [R]"),
        ]
        self.chat_output = ChatOutput()
        self.outputs = [self.chat_output]

        self.category = ChatCategory
        self.sub = "Chat Viewers"
        self.name = "Chat Component"


        self.subscription = None

        self.chatbot_input: AsyncSubject = None     # type: ignore
        # gets the string message that the user types in
        self.user_msg_input: AsyncSubject = None    # type: ignore
        self.info = "Chat chat chat."

        self.chatbot_msg_forwarder = ReactiveForwarder(self.chat_output, 'msg_from_chatbot')

        self.side_effects = True

    def run(self, info: str, chatbot: AsyncSubject, user_msg: AsyncSubject) -> str:
        """
            `user_output` receives messages from the user
            `chatbot_input` sends messages to the chatbot ui
        """
        self.info = info
        self.chatbot_input = chatbot
        # used to send the user message to the node the provides
        self.user_msg_input = user_msg
        logger.info(f"subjectx: {self.chatbot_input} {self.user_msg_input}")

        return ''

    async def run_async(self):
        # subscribes to and sends the message received on the chatbot input
        await asyncio.sleep(1)
        if self.subscription is None:
            self.subscription = await self.chatbot_input.subscribe_async(self.chatbot_msg_forwarder)
            await self.send_ui_event(MsgFromChatbot(msg=self.info))
        logger.info(f"subject2: {self.chatbot_input} {self.user_msg_input}")

        while True:
            received: MsgFromUser = await self.receive_ui_event()
            if received['msg'] == 'quit':
                break
            await self.user_msg_input.asend(("msg_from_user", received))

    async def send_ui_event(self, message: MsgFromChatbot):
        channel_id = self.chat_output.get_channel_id_by_name('msg_from_chatbot')

        out_message = ToUIOutputMessage(channel_id=channel_id,
                                        data=message,
                                        message_tag="msg_from_chatbot")
        await self.chat_output.send_ui_event(event=out_message)

    async def receive_ui_event(self) -> MsgFromUser:
        event = await self.chat_output.receive_ui_event(channel_name='msg_from_user')
        return event['data']
