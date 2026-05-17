from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(override=True)

# Debug API key
#print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

from agents import Agent, Runner

# Single Agent
coding_agent = Agent(
    name="coding_agent",
    instructions="""
    You are an expert software developer.
    
    You can answer questions related to:
    - Python
    - Java
    - Exception Handling
    - OOPs
    - APIs
    - Data Structures
    - Programming Best Practices
    
    Provide clear and beginner-friendly explanations.
    """
)

# User Query
query = input("Ask your programming question: ")

# Run Agent
response = Runner.run_sync(
    coding_agent,
    query
)

# Final Output
print("\nFinal Output:\n")
print(response.final_output)