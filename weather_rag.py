import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Debug Keys
#print("Weather API Key Loaded:", WEATHER_API_KEY)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# User Input
city = input("Enter city name: ")

# Weather API URL
url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"


# Call Weather API
response = requests.get(url)

# Convert response into JSON
weather_data = response.json()

# Debug Full API Response
print("\nAPI Response:")
print(weather_data)

# Validate API response
if response.status_code != 200:
    print("\nError:", weather_data.get("message"))
    exit()

# Extract weather details safely
temperature = weather_data["current"]["temp_c"]
description = weather_data["current"]["condition"]["text"]
humidity = weather_data["current"]["humidity"]

# Retrieved Context
context = f"""
City: {city}
Temperature: {temperature}°C
Weather: {description}
Humidity: {humidity}%
"""

print("\nRetrieved Weather Data:")
print(context)

# Prompt for LLM
prompt = f"""
You are a weather assistant.

Using the following weather data,
generate a simple user-friendly weather summary.

Weather Data:
{context}
"""

# OpenAI Response
chat_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Final Output
print("\nAI Response:\n")
print(chat_response.choices[0].message.content)