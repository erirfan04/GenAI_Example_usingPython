from openai import OpenAI
from dotenv import load_dotenv
import os

# Force reload .env and override old system variables
load_dotenv(override=True)

# Debug print
#print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

topic = input("Enter email topic: ")

prompt = f"""
Write a professional email about:
{topic}
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nGenerated Email:\n")
print(response.choices[0].message.content)