from chromadb.api.models import Collection
from sanic.log import logger

from ..chroma import category as ChromaDB
from ..chat.io.chroma_collection import ChromaCollectionOutput, ChromaCollectionInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory


@NodeFactory.register("machines:chroma:chroma_search")
class ChromaSearch(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Searches a chroma collection for matches."
        self.inputs = [
            ChromaCollectionInput(label="-> Collection"),
        ]
        self.outputs = [ChromaCollectionOutput(label="Collection ->")]

        self.category = ChromaDB
        self.sub = "Chroma Collection"
        self.name = "Search"

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

