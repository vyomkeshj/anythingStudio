import os

from langchain.chat_models import ChatOpenAI

from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from sqlalchemy import create_engine

if __name__ == '__main__':

    os.environ["OPENAI_API_KEY"] = "DsUoLtHg1IGhwvAgN78PT3BlbkFJpkBNvED6fl7lhjWtL1jB"
    question = "how many products do we have?"
    try:
        db = SQLDatabase.from_uri("mysql+mysqlconnector://vyomkesh:$$5678Vyom!!@drinksmate.cbl2ralli4lr.ap-southeast-2.rds.amazonaws.com:3306/drinksmate")
        # llm = OpenAI(temperature=0, model_name="text-davinci-003")
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
        answer = db_chain.run(question)
        print(answer)
    except Exception as error:
        print(f"{error}")
