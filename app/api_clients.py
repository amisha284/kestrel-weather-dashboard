"""Small API clients for location lookup and current weather."""

import math
import os

import requests


class APIError(Exception):
    """An API problem that can be explained to the user."""


def validate_weather(data):
    """Check the weather fields used by the clients, scoring and formatting."""
    try:
        temperature = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        conditions = data["weather"]
        rain = data.get("rain", {})
        if not isinstance(conditions, list) or not conditions or not isinstance(rain, dict):
            raise ValueError

        numbers = [temperature, wind_speed]
        if "1h" in rain:
            numbers.append(rain["1h"])
        if "dt" in data:
            numbers.append(data["dt"])
        for value in numbers:
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError
        if wind_speed < 0 or rain.get("1h", 0) < 0:
            raise ValueError

        for condition in conditions:
            if (
                not isinstance(condition, dict)
                or type(condition["id"]) is not int
                or not isinstance(condition["description"], str)
                or not condition["description"].strip()
            ):
                raise ValueError
    except (KeyError, IndexError, TypeError, ValueError, OverflowError):
        raise APIError("OpenWeatherMap returned incomplete or invalid weather data.") from None


class BaseClient:
    """Share credential loading and HTTP error handling between both clients."""

    def __init__(self, credential_name):
        # Keep credentials inside the client rather than passing them to the UI.
        self._credential = os.getenv(credential_name, "").strip()
        if not self._credential:
            raise APIError(f"Set {credential_name} in your environment or .env file.")

    def _get_json(self, url, params):
        """Request a JSON object, without including secret URLs in errors."""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.Timeout:
            raise APIError("The API request timed out. Please try again.") from None
        except requests.HTTPError as error:
            status = error.response.status_code
            if status in (401, 403):
                message = "The API rejected the credentials. Check your key and permissions."
            elif status == 429:
                message = "The API request limit was reached. Please try again later."
            else:
                message = f"The API request failed (HTTP {status}). Please try again later."
            raise APIError(message) from None
        except requests.RequestException:
            raise APIError("Could not connect to the API. Check your connection.") from None

        try:
            data = response.json()
        except ValueError:
            raise APIError("The API returned invalid JSON.") from None
        if not isinstance(data, dict):
            raise APIError("The API returned an unexpected response format.")
        return data


class MapboxClient(BaseClient):
    """Convert a location name into coordinates using Mapbox Geocoding v6."""

    def __init__(self):
        super().__init__("MAPBOX_ACCESS_TOKEN")

    def geocode(self, location):
        """Return the first matching location as name, latitude and longitude."""
        if not isinstance(location, str) or not location.strip():
            raise APIError("Enter a location name, such as Perth, Australia.")
        location = location.strip()
        if len(location) > 256 or ";" in location:
            raise APIError("Use a location name of at most 256 characters without semicolons.")

        data = self._get_json(
            "https://api.mapbox.com/search/geocode/v6/forward",
            {
                "q": location,
                "access_token": self._credential,
                "limit": 1,
                "autocomplete": "false",
            },
        )
        features = data.get("features")
        if not isinstance(features, list):
            raise APIError("Mapbox returned an unexpected location response.")
        if not features:
            raise APIError("No matching location was found. Try adding a country name.")

        try:
            feature = features[0]
            coordinates = feature["geometry"]["coordinates"]
            longitude, latitude = coordinates
            name = feature["properties"]["full_address"]
            if (
                type(latitude) not in (int, float)
                or type(longitude) not in (int, float)
                or not (-90 <= latitude <= 90 and -180 <= longitude <= 180)
                or not isinstance(name, str)
                or not name.strip()
            ):
                raise ValueError
        except (KeyError, IndexError, TypeError, ValueError):
            raise APIError("Mapbox returned incomplete or invalid location data.") from None

        # Mapbox supplies longitude first; weather requests use named coordinates.
        return {"name": name, "latitude": latitude, "longitude": longitude}


class WeatherClient(BaseClient):
    """Fetch current OpenWeatherMap data in Celsius and metres per second."""

    def __init__(self):
        super().__init__("OPENWEATHER_API_KEY")

    def get_weather(self, latitude, longitude):
        """Return the provider's weather payload after checking its core fields."""
        if (
            type(latitude) not in (int, float)
            or type(longitude) not in (int, float)
            or not (-90 <= latitude <= 90 and -180 <= longitude <= 180)
        ):
            raise APIError("Latitude must be between -90 and 90; longitude between -180 and 180.")

        data = self._get_json(
            "https://api.openweathermap.org/data/2.5/weather",
            {"lat": latitude, "lon": longitude, "appid": self._credential, "units": "metric"},
        )
        validate_weather(data)
        return data
