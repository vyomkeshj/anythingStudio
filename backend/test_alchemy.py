import os

from langchain.chat_models import ChatOpenAI

from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from sqlalchemy import create_engine
from langchain.prompts.prompt import PromptTemplate
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

Select 20 maximum at a time because otherwise the output becomes too big.

Question: {input}"""


if __name__ == '__main__':
    print("coming in hot")
    os.environ["OPENAI_API_KEY"] = "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"
    question = "how many products do we have?"
    try:
        db = SQLDatabase.from_uri("mysql+mysqlconnector://vyomkesh:$$5678Vyom!!@drinksmate.cbl2ralli4lr.ap-southeast-2.rds.amazonaws.com:3306/drinksmate")
        # llm = OpenAI(temperature=0, model_name="text-davinci-003")
        print("connection established")

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        print("bro")
        input = "how many products do we have?"
        table_info = ['products', 'orders']
        dialect = 'MySQL'
        PROMPT = PromptTemplate(
            input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
        )

        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_intermediate_steps=True, prompt=PROMPT)
        print("bro 2")
        answer = db_chain.run(question)
        print(answer)
    except Exception as error:
        print(f"{error}")
