"""Run with: python -m scripts.check_apis "Perth, Australia"."""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from app.api_clients import APIError, MapboxClient, WeatherClient


def main():
    parser = argparse.ArgumentParser(description="Check both Kestrel API integrations.")
    parser.add_argument("location", help="Location name, for example 'Perth, Australia'")
    args = parser.parse_args()
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    try:
        # Validate both keys before making any paid or rate-limited requests.
        mapbox = MapboxClient()
        weather_client = WeatherClient()
        location = mapbox.geocode(args.location)
        weather = weather_client.get_weather(location["latitude"], location["longitude"])
    except APIError as error:
        parser.exit(1, f"API check failed: {error}\n")

    print(f"Location: {location['name']}")
    print(f"Coordinates: {location['latitude']}, {location['longitude']}")
    print(f"Conditions: {weather['weather'][0]['description']}")
    print(f"Temperature: {weather['main']['temp']} °C")
    print(f"Wind speed: {weather['wind']['speed']} m/s")
    print("Both API checks passed.")


if __name__ == "__main__":
    main()
