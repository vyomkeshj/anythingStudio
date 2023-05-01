from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.agents import Tool

from .io.plugins import PluginOutput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...nodes.langchain import category as LangchainCategory


@NodeFactory.register("machines:langchain:todo_list_plugin")
class PythonReplTool(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Langchain todo list plugin."

        self.outputs = [PluginOutput(label="Todo Plugin ->", output_type="string")]

        self.category = LangchainCategory
        self.sub = "Plugins"
        self.name = "Todo List"

        self.side_effects = True

    def run(self, ) -> Tool:
        """Creates a list of tools from the inputs."""
        todo_prompt = PromptTemplate.from_template(
            "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}"
        )
        todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
        return Tool(
            name="TODO",
            func=todo_chain.run,
            description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
        )

    async def run_async(self):
        pass
