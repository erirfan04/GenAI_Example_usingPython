from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Debug API Key
#print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

from agents import Agent, Runner

# -----------------------------
# Python Agent
# -----------------------------
python_agent = Agent(
    name="python_agent",
    instructions="""
    You are an expert Python developer.
    
    Help users with:
    - Python syntax
    - OOPs
    - Exception handling
    - APIs
    - NumPy
    - Pandas
    - FastAPI
    
    Provide beginner-friendly explanations.
    """,
    handoff_description="Handles Python-related queries"
)

# -----------------------------
# Java Agent
# -----------------------------
java_agent = Agent(
    name="java_agent",
    instructions="""
    You are an expert Java developer.
    
    Help users with:
    - Java syntax
    - OOPs
    - Collections
    - Exception handling
    - Multithreading
    - Spring Boot
    
    Provide clear explanations with examples.
    """,
    handoff_description="Handles Java-related queries"
)

# -----------------------------
# SQL Agent
# -----------------------------
sql_agent = Agent(
    name="sql_agent",
    instructions="""
    You are an SQL database expert.
    
    Help users with:
    - SQL queries
    - Joins
    - Subqueries
    - Indexes
    - Normalization
    - Stored procedures
    
    Explain using real-world examples.
    """,
    handoff_description="Handles SQL and database queries"
)

# -----------------------------
# Routing Agent
# -----------------------------
routing_agent = Agent(
    name="routing_agent",
    instructions="""
    Your job is to determine which specialized agent
    should answer the user's question.
    
    Route:
    - Python questions → python_agent
    - Java questions → java_agent
    - SQL/Database questions → sql_agent
    """,
    handoffs=[
        python_agent,
        java_agent,
        sql_agent
    ]
)

# -----------------------------
# User Input
# -----------------------------
query = input("Ask your question: ")

# -----------------------------
# Run Multi-Agent System
# -----------------------------
response = Runner.run_sync(
    routing_agent,
    query
)

# -----------------------------
# Final Output
# -----------------------------
print("\nFinal Output:\n")
print(response.final_output)