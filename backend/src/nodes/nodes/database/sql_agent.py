from typing import Tuple, List

from aioreactive import AsyncSubject, AsyncObserver
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from openai_async import openai_async
from sanic.log import logger

from . import category as DatabaseCategory
from ..chat.impl.protocol import MsgHistoryItem, MsgFromChatbot
from ...io.inputs import SliderInput
from ...io.outputs.signal_output import SignalOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory


@NodeFactory.register("machines:dbase:sql_builder")
class SQLAgentNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain sql agent."

        self.inputs = [
            SliderInput(
                "Completion Len",
                minimum=30,
                maximum=300,
                default=30,
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
        self.outputs = [SignalOutput(label="[R] history in <-"), SignalOutput(label="[R] next msg out ->")]

        self.category = DatabaseCategory
        self.sub = "Langchain"
        self.name = "MySQL Oracle"
        self.uri = None

        self.agentExecutor = None
        self.database = None
        self.toolkit = None

        self.history_in = AsyncSubject()
        self.nxt_msg_out = AsyncSubject()

        self.history_input_sub = None
        self.side_effects = True
        self.input_listener = None
        self.listener_subscription = None
        self.controller = SQLMaker(self)


    def run(self, completion_len: float) -> Tuple[AsyncSubject, AsyncSubject]:
        self.uri = f"mysql+pymysql://vyomkesh:$$5678Vyom!!@drinksmate.cbl2ralli4lr.ap-southeast-2.rds.amazonaws.com:{3306}/drinksmate"
        print(f"uri: {self.uri}")

        return self.history_in, self.nxt_msg_out

    async def run_async(self):
        print("run async")
        self.database = SQLDatabase.from_uri(self.uri)
        self.toolkit = SQLDatabaseToolkit(db=self.database, llm=OpenAI(temperature=0, model_name="gpt-4"))

        self.agentExecutor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=self.toolkit,
            verbose=True,
            return_intermediate_steps=True,
        )
        if self.history_input_sub is None:
            self.history_input_sub = await self.history_in.subscribe_async(self.controller)


class SQLMaker(AsyncObserver):

    def __init__(self, state_node: SQLAgentNode):
        super().__init__()
        self.state_node: SQLAgentNode = state_node

    async def asend(self, input_hist: List[MsgHistoryItem]) -> None:
        # input_hist.insert(0, {"role": "system", "content": self.state_node.system_message})
        last_message = ""
        if len(input_hist) > 0:
            last_message = input_hist[-1]
            last_content = last_message["content"]
            response = self.state_node.agentExecutor.run({"input": last_content})
            logger.info(f"response: {response}")
            await self.state_node.nxt_msg_out.asend(("msg_from_chatbot", MsgFromChatbot(msg=response)))

        else:
            raise Exception("No choices in response")


    async def athrow(self, error: Exception) -> None:
        print("Error:", error)

    async def aclose(self) -> None:
        print("Stream closed")
