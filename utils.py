from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Debug key
#print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

from agents import Agent, Runner
from tool import get_current_weather
from pydantic import BaseModel

# Output schema
class Weather(BaseModel):
    location: str
    temperature: float

# Create Weather Agent
agent = Agent(
    name="weather_agent",

    instructions="""
    You are an expert weather assistant.

    Use weather tool to fetch live weather.
    Return structured output.
    """,

    tools=[get_current_weather],

    model="gpt-4o-mini",

    output_type=Weather
)

# Run Agent
response = Runner.run_sync(
    agent,
    "What is the weather in London?"
)

# Final Output
print("\nFinal Output:\n")
print(response.final_output)