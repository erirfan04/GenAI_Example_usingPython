from dotenv import load_dotenv
load_dotenv(override=True)

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from langchain.agents import (
    AgentExecutor,
    create_openai_tools_agent
)

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain.memory import ConversationBufferMemory


# --------------------------------------
# TOOL 1 - Download CSV
# --------------------------------------
@tool
def download_sales_data(dummy: str = "") -> str:
    """
    Downloads sales CSV file.
    """
    url="https://drive.google.com/uc?export=download&id=1x4UDtoONLJnA_MT093FaeBaLpntYaXPl"
    response = requests.get(url)

    with open("sales_data.csv", "wb") as f:
        f.write(response.content)

    return "sales_data.csv downloaded successfully."


# --------------------------------------
# TOOL 2 - Analyze CSV
# --------------------------------------
@tool
def analyze_sales_data(file_path: str) -> str:
    """
    Reads CSV and analyzes sales data.
    """

    df = pd.read_csv(file_path)

    summary = df.describe().to_string()

    return summary


# --------------------------------------
# TOOL 3 - Create Chart
# --------------------------------------
@tool
def create_sales_chart(file_path: str) -> str:
    """
    Creates sales chart visualization.
    """

    df = pd.read_csv(file_path)

    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) == 0:
        return "No numeric columns found."

    column = numeric_cols[0]

    plt.figure(figsize=(8,5))

    plt.plot(df[column])

    plt.title(f"{column} Trend")

    plt.xlabel("Index")

    plt.ylabel(column)

    plt.savefig("sales_chart.png")

    plt.close()

    return "Chart saved as sales_chart.png"


# --------------------------------------
# TOOL 4 - Email Report
# --------------------------------------
@tool
def email_report(dummy: str = "") -> str:
    """
    Emails sales chart report.
    """
    receiver_email = "er.irfan041@gmail.com"
    sender_email = os.getenv("EMAIL_USER")

    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()

    msg["Subject"] = "AI Generated Sales Report"

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg.set_content(
        "Please find attached AI-generated sales report chart."
    )

    with open("sales_chart.png", "rb") as f:

        file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="image",
            subtype="png",
            filename="sales_chart.png"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(sender_email, sender_password)

        smtp.send_message(msg)

    return "Email report sent successfully."


# --------------------------------------
# MEMORY
# --------------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# --------------------------------------
# LLM MODEL
# --------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# --------------------------------------
# TOOLS
# --------------------------------------
tools = [
    download_sales_data,
    analyze_sales_data,
    create_sales_chart,
    email_report
]


# --------------------------------------
# PROMPT TEMPLATE
# --------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [

        (
            "system",

            """
You are an Autonomous Workflow AI Agent.

You can:
- download files
- analyze CSV data
- create charts
- send email reports
- execute tasks step-by-step autonomously
"""
        ),

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        (
            "human",
            "{input}"
        ),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),
    ]
)


# --------------------------------------
# CREATE AGENT
# --------------------------------------
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# --------------------------------------
# AGENT EXECUTOR
# --------------------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)


# --------------------------------------
# CHAT LOOP
# --------------------------------------
print("\nAutonomous Workflow Agent Started")
print("Type 'exit' to stop\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":

        print("Agent: Goodbye")
        break

    response = agent_executor.invoke({
        "input": user_input
    })

    print("\nAgent Response:")
    print("--------------------------------")
    print(response["output"])
    print("--------------------------------\n")