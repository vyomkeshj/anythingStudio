import asyncio
from typing import Tuple, List, Optional, Union

from aioreactive import AsyncSubject, AsyncObserver
from langchain import OpenAI
from langchain.agents import Tool
from langchain.embeddings import OpenAIEmbeddings
from reactivex import Subject
from sanic.log import logger

from .babyagi.babyagi import BabyAGI
from .impl.protocol import MsgFromUser, MsgFromChatbot
from .openai_chatbot import OAIChatbot
from src.nodes.nodes.chat.io.plugins import PluginListInput
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import SliderInput
from . import category as ChatCategory
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

import faiss


@NodeFactory.register("machines:chat:bubbagi_agent")
class BabyAgiNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Baby AGI Node."
        self.inputs = [
            PluginListInput(label="Plugins List ->"),
            SliderInput(
                "Completion Len",
                minimum=30,
                maximum=3000,
                default=300,
                precision=1,
                controls_step=1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ]),
            SliderInput(
                "Temperature",
                minimum=0.1,
                maximum=1,
                default=0.2,
                precision=1,
                controls_step=0.1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ]),
            SliderInput(
                "#Attempts",
                minimum=1,
                maximum=5,
                default=1,
                precision=1,
                controls_step=1,
                gradient=[
                    "#ff0000",
                    "#ffff00",
                    "#00ff00",
                    "#00ffff",
                    "#0000ff",
                    "#ff00ff",
                    "#ff0000",
                ]),
        ]
        self.outputs = [SignalOutput(label="-> [R] bot msg out"), SignalOutput(label="<- usr msg in [R]")]

        self.bot_msg_output: AsyncSubject = AsyncSubject()
        self.usr_nxt_msg_in: AsyncSubject = AsyncSubject()

        self.category = ChatCategory
        self.sub = "AutoGPT v0.1"
        self.name = "Auto GPT"

        self.baby_agi = None
        self.completion_len = 150
        self.controller = None

        self.api_key = None
        self.objective: str = None  # type: ignore
        self.observer = None
        self.subscription = None

        self.info = "The taskmaster."
        self.babyagi_observer = Subject()

        self.side_effects = True

    def run(self, tools_list: List[Tool], completion_len: float, temp: float, attempts: float) -> Tuple[AsyncSubject, AsyncSubject]:
        """
            baby agi node
        """
        self.completion_len = completion_len
        self.api_key = "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"

        # Define your embedding model
        embeddings_model = OpenAIEmbeddings()
        # Initialize the vectorstore as empty

        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vector_store = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

        # Logging of LLMChains
        llm = OpenAI(temperature=temp, api_key=self.api_key)
        # llm = OpenAI(temperature=temp, api_key=self.api_key, )

        verbose = True
        # If None, will keep on going forever
        max_iterations: Optional[int] = int(attempts)
        self.baby_agi = BabyAGI.from_llm(
            llm=llm, vectorstore=vector_store, verbose=verbose, max_iterations=max_iterations, tool_list=tools_list
        )
        self.observer = MessageObserver(self)
        logger.info(f"the subjects are: {self.bot_msg_output}, {self.usr_nxt_msg_in}")
        return self.bot_msg_output, self.usr_nxt_msg_in

    async def run_async(self):
        if self.subscription is None:
            self.subscription = await self.usr_nxt_msg_in.subscribe_async(self.observer)
        await asyncio.sleep(0.2)


class MessageObserver(AsyncObserver):

    def __init__(self, state_node: OAIChatbot):
        super().__init__()
        self.state_node: OAIChatbot = state_node

    async def asend(self, input_msg: Tuple[str, Union[MsgFromUser, MsgFromChatbot]]) -> None:
        logger.info(f"Received {input_msg} in state node")
        if input_msg[0] == "msg_from_user":
            # run babyagi
            if self.state_node.objective is None:
                self.state_node.objective = input_msg[1]["msg"]
                self.state_node.baby_agi({"objective": input_msg[1]["msg"]})
                result = self.state_node.baby_agi.get_result()
                if result:
                    logger.info(f"Final response: {result}")
                    await self.state_node.bot_msg_output.asend(MsgFromChatbot(msg=str(result)))
                self.state_node.objective = None
            else:
                await self.state_node.bot_msg_output.asend(MsgFromChatbot(msg="I'm busy right now, please wait a bit."))
        else:
            logger.error(f"Received {input_msg} in state node from unknown source")

    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")
