import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()  # Load environment variables from .env file

# Load and normalize the debug variable from environment
debug = os.getenv("DEBUG", "false").lower()

city = input("Enter a city name: ")

headers = {
    "User-Agent": "MinijobMailerBot/1.0 (info@niklasmetzger.de)",
    "Referer": "https://github.com/nikla/minijob-mailer",
}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": city, "format": "json"},
    headers=headers,
)

if debug == "true":
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

if response.status_code == 200:
    try:
        json_data = response.json()
        if debug == "true":
            print(json_data)

        # Check if the list contains any results
        if json_data:
            lat = json_data[0]["lat"]
            lon = json_data[0]["lon"]
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print(f"No coordinates found for city: '{city}'")

    except requests.exceptions.JSONDecodeError:
        print("Failed to decode response as JSON.")
else:
    print(f"Request failed or was blocked. Status code: {response.status_code}")