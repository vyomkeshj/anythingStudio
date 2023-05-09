from langchain import PromptTemplate, LLMChain
from langchain.llms import BaseLLM

from src.nodes.nodes.chat.babyagi.prompts import task_prioritization_template


class TaskPrioritizationChain(LLMChain):
    """Chain to prioritize tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, task_prioritization_template: str, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=task_prioritization_template,
            input_variables=["task_names", "next_task_id", "objective"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)