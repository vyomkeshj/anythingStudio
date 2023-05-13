from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM


class TaskCreationChain(LLMChain):
    """Chain to generates tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, task_creation_template: str, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=task_creation_template,
            input_variables=[
                "result",
                "task_description",
                "incomplete_tasks",
                "objective",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
