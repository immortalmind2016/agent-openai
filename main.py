from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from langchain.schema import SystemMessage
from tools.report import write_report_tool
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handler import ChatModelStartHandler
from tools.sql import run_query_tool,list_tables,describe_tables_tool

load_dotenv()

chat = ChatOpenAI(
    callbacks=[ChatModelStartHandler()],
)

tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [
    run_query_tool,
    describe_tables_tool,
    write_report_tool
]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    # verbose=True,
    tools=tools,
    memory=memory
)

agent_executor(
    "How many orders are there? Write the result to an html report."
)

agent_executor(
    "Repeat the exact same process for users and create a new file called users.html."
)
