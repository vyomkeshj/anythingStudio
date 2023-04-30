from typing import Tuple, List, Optional

from aioreactive import AsyncSubject
from langchain import OpenAI
from langchain.agents import Tool
from langchain.embeddings import OpenAIEmbeddings
from sanic.log import logger

from .babyagi.babyagi import BabyAGI
from ..langchain.io.tools import ToolListInput
from ...io.outputs import TextOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import SliderInput, TextInput
from . import category as ChatCategory
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

import faiss


@NodeFactory.register("machines:chat:bubbagi_agent")
class OAIChatbot(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "BubbaAGI."
        self.inputs = [
            TextInput(label="Task"),
            ToolListInput(label="Tools List ->"),
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
                default=0.7,
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
        ]
        self.outputs = [TextOutput(label="agi response->")]

        self.category = ChatCategory
        self.sub = "AGI"
        self.name = "Bubba AGI"
        self.icon = "BsFillDatabaseFill"

        self.completion_len = 150
        self.controller = None

        self.api_key = None
        self.system_message: str = ''   # type: ignore

        self.info = "The taskmaster."

        self.side_effects = True

    def run(self, system_message: str, tools_list: List[Tool], completion_len: float, temp: float) -> str:
        """
            Initializes the controller
        """
        self.completion_len = completion_len
        self.api_key = "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"
        self.system_message = system_message

        # Define your embedding model
        embeddings_model = OpenAIEmbeddings()
        # Initialize the vectorstore as empty

        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vector_store = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

        # Logging of LLMChains
        llm = OpenAI(temperature=temp, api_key=self.api_key, model_name="gpt-4")

        verbose = True
        # If None, will keep on going forever
        max_iterations: Optional[int] = 3
        baby_agi = BabyAGI.from_llm(
            llm=llm, vectorstore=vector_store, verbose=verbose, max_iterations=max_iterations, tool_list=tools_list
        )
        response = baby_agi({"objective": system_message})
        logger.info(f"BubbaAGI Response: {response}")

        return 'response'

    async def run_async(self):
        logger.info("Running BubbaAGI")
