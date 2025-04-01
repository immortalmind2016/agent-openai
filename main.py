from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from langchain.schema import SystemMessage


from tools.sql import run_query_tool,describe_table_tool

load_dotenv()

chat=ChatOpenAI()

def list_tables() -> str:
    c=conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    row = c.fetchall()
    return "\n".join([table[0] for table in row])
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage("You are a SQL expert. You can run SQL queries on the example.db database.\n"
                      f"the database has the following tables: {list_tables()}\n"
                      "Don't make assumptions about the table names."
                      "If you need to know the table structure, use the 'describe_table' function."),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]

)
tools=[run_query_tool,describe_table_tool]
agent=OpenAIFunctionsAgent(
    llm=chat,
    tools=[run_query_tool],
    prompt=prompt,
    verbose=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[run_query_tool],
    verbose=True
)

agent_executor.run("How many users are there in the database?")