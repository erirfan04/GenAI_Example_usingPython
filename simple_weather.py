import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

print("Loaded Key:", WEATHER_API_KEY)

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

response = requests.get(url)

print("Status Code:", response.status_code)

weather_data = response.json()

print("API Response:", weather_data)

# Validate API response
if response.status_code != 200:
    print("API Error:", weather_data.get("message"))
    exit()

temperature = weather_data["main"]["temp"]

print("Temperature:", temperature)