from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool

load_dotenv()

chat=ChatOpenAI()

prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]

)

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