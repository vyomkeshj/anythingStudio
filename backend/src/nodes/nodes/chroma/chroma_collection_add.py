from chromadb.api.models import Collection

from ...nodes.chroma import category as ChromaDB
from ...nodes.chat.io.chroma_collection import ChromaCollectionOutput, ChromaCollectionInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory


@NodeFactory.register("machines:chroma:chroma_add")
class ChromaAdd(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Creates a chroma collection with the given name."
        self.inputs = [
            ChromaCollectionInput(label="-> Collection"),
        ]
        self.outputs = [ChromaCollectionOutput(label="Collection ->")]

        self.category = ChromaDB
        self.sub = "Chroma Collection"
        self.name = "Add"


        self.hasEffects = True

        # self.info = "Stores the state of the chat box."


    def run(self, collection: Collection) -> Collection:
        """
            Creates a chroma collection and returns it. (remember runs auto when drooped in)
        """
        collection.add(
            documents=["This is document1", "This is document2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
            metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
            ids=["doc1", "doc2"], # unique for each doc
        )
        return collection

    async def run_async(self):
        pass

