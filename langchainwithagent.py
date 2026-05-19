from dotenv import load_dotenv
load_dotenv(override=True)

import datetime
import pandas as pd

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


# -----------------------------------
# TOOL 1 - Current Time Tool
# -----------------------------------
@tool
def get_current_time(dummy: str = "") -> str:
    """Returns current date and time."""
    return str(datetime.datetime.now())


# -----------------------------------
# TOOL 2 - Calculator Tool
# -----------------------------------
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------------
# TOOL 3 - CSV Analyzer
# -----------------------------------
@tool
def analyze_csv(file_path: str) -> str:
    """Reads a CSV file and returns column averages."""
    try:
        df = pd.read_csv(file_path)

        numeric_means = df.mean(numeric_only=True)

        return numeric_means.to_string()

    except Exception as e:
        return f"Error reading CSV: {str(e)}"


# -----------------------------------
# MEMORY
# -----------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# -----------------------------------
# MODEL
# -----------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# -----------------------------------
# TOOLS
# -----------------------------------
tools = [
    get_current_time,
    calculator,
    analyze_csv
]


# -----------------------------------
# PROMPT
# -----------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant with tool calling abilities."
        ),

        MessagesPlaceholder(variable_name="chat_history"),

        ("human", "{input}"),

        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# -----------------------------------
# CREATE AGENT
# -----------------------------------
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# -----------------------------------
# AGENT EXECUTOR
# -----------------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)


# -----------------------------------
# CHAT LOOP
# -----------------------------------
print("\nAdvanced LangChain Agent Started")
print("Type 'exit' to stop\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye")
        break

    response = agent_executor.invoke({
        "input": user_input
    })

    print("\nBot Response:")
    print("--------------------------------")
    print(response["output"])
    print("--------------------------------\n")