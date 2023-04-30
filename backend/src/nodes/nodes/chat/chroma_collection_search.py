from chromadb.api.models import Collection
from sanic.log import logger

from . import category as ChatCategory
from .io.chroma_collection import ChromaCollectionOutput, ChromaCollectionInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory


# some way to just tag this as websocket node?
@NodeFactory.register("machines:chat:chroma_search")
class ChatState(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Searches a chroma collection for matches."
        self.inputs = [
            ChromaCollectionInput(label="-> Collection"),
        ]
        self.outputs = [ChromaCollectionOutput(label="Collection ->")]

        self.category = ChatCategory
        self.sub = "Chroma Collection"
        self.name = "Search"
        self.icon = "BsFillDatabaseFill"
        self.hasEffects = True

        # self.info = "Stores the state of the chat box."


    def run(self, collection: Collection) -> Collection:
        """
            Creates a chroma collection and returns it. (remember runs auto when drooped in)
        """
        results = collection.query(
            query_texts=["This is a query document"],
            n_results=2,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        logger.info(f"Search results: {results}")
        return collection
    
    async def run_async(self):
        pass

