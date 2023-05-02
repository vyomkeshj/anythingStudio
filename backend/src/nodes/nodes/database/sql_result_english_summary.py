import openai

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import TextInput
from ...io.outputs import TextOutput
from . import category as DatabaseCategory

template = """Act like you are a bartender. Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""


@NodeFactory.register("machines:image:summarizer")
class MySQLQueryNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Try to answer based on a input document and gpt-3.5"
        self.inputs = [
            TextInput("Question"),
            TextInput("-> HTML In"),
        ]
        self.outputs = [TextOutput("Markdown Response ->")]

        self.category = DatabaseCategory
        self.sub = "Natural Language"
        self.name = "Result Summarizer"


        self.side_effects = True

    def run(self, secret: str, question: str, sql_run_out: str) -> str:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who summarises the output of SQL execution "
                                              "in natural language. The output should not contain the table."},
                {"role": "system", "content": "Output only beautifully formatted markdown"},
                {"role": "assistant", "content": f"the data output is: {sql_run_out} and the user's question was: {question}"},
            ]
        )
        return response['choices'][0]['message']['content'].strip()

