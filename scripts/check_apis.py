"""Run with: python -m scripts.check_apis "Perth, Australia"."""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from app.api_clients import APIError
from app.weather_analysis import get_weather_report


def main():
    parser = argparse.ArgumentParser(description="Check the Kestrel weather and risk report.")
    parser.add_argument("location", help="Location name, for example 'Perth, Australia'")
    args = parser.parse_args()
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    try:
        report = get_weather_report(args.location)
    except APIError as error:
        parser.exit(1, f"API check failed: {error}\n")

    print(f"Location: {report['location']}")
    print(f"Coordinates: {report['latitude']}, {report['longitude']}")
    print(f"Conditions: {report['conditions']}")
    print(f"Temperature: {report['temperature']}")
    print(f"Wind speed: {report['wind_speed']}")
    print(f"Rainfall: {report['rainfall']}")
    print(f"Observed at: {report['observed_at']}")
    print(f"Risk level: {report['risk_level']}")
    for reason in report["risk_reasons"]:
        print(f"- {reason}")
    print("Both API checks passed.")


if __name__ == "__main__":
    main()
