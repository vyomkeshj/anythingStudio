import chromadb
from chromadb.api.models import Collection
from sanic.log import logger

from . import category as ChatCategory
from .io.chroma_collection import ChromaCollectionOutput
from ...io.inputs import TextInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chat:chroma_create")
class PineconeCreate(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Gets or Creates a chroma collection."
        self.inputs = [
            TextInput(label="Collection Name"),
        ]
        self.outputs = [ChromaCollectionOutput(label="Collection ->")]

        self.category = ChatCategory
        self.sub = "Chroma Collection"
        self.name = "Get/Create"
        self.icon = "BsFillDatabaseFill"
        self.subject = None
        # self.info = "Stores the state of the chat box."

        self.hasEffects = True
        self.client = None
        self.collection = None


    def run(self, collection_name: str) -> Collection:
        """
            Creates a chroma collection and returns it. (remember runs auto when drooped in)
        """

        try:
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(collection_name)
            logger.info(f"Created collection {self.collection}")
        except Exception as e:
            logger.info("Error creating collection")
            print(e)

        return self.collection

    async def run_async(self):
        pass

