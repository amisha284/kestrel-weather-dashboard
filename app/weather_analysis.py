"""Simple coursework rules and display formatting for current weather."""

from datetime import datetime, timezone

from app.api_clients import APIError, MapboxClient, WeatherClient, validate_weather


class RiskEngine:
    """Assign Low, Medium or High using fixed thresholds and explain the result."""

    def assess(self, weather):
        validate_weather(weather)
        wind = weather["wind"]["speed"]
        rain = weather.get("rain", {}).get("1h", 0)
        level = "Low"
        reasons = []

        # Prototype thresholds, not a validated logistics risk model.
        if wind >= 15:
            level = "High"
            reasons.append(f"High wind speed ({wind:.1f} m/s).")
        elif wind >= 8:
            level = "Medium"
            reasons.append(f"Elevated wind speed ({wind:.1f} m/s).")

        if rain >= 7.5:
            level = "High"
            reasons.append(f"Heavy rainfall ({rain:.1f} mm/h).")
        elif rain >= 2.5:
            if level == "Low":
                level = "Medium"
            reasons.append(f"Elevated rainfall ({rain:.1f} mm/h).")

        for condition in weather["weather"]:
            if 200 <= condition["id"] <= 299:
                level = "High"
                reasons.append("Thunderstorm conditions reported.")
                break

        if not reasons:
            reasons.append("No configured risk thresholds exceeded.")
        return {"level": level, "reasons": reasons}


class DataFormatter:
    """Turn validated API data and a risk assessment into a display dictionary."""

    def format(self, location, weather, assessment):
        validate_weather(weather)
        rain = weather.get("rain", {})
        observed_at = "Unavailable"
        if "dt" in weather:
            try:
                observed_at = datetime.fromtimestamp(weather["dt"], timezone.utc).strftime(
                    "%Y-%m-%d %H:%M UTC"
                )
            except (ValueError, OverflowError, OSError):
                raise APIError("OpenWeatherMap returned an invalid observation time.") from None

        return {
            "location": location["name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "conditions": weather["weather"][0]["description"],
            "temperature": f"{weather['main']['temp']:.1f} °C",
            "wind_speed": f"{weather['wind']['speed']:.1f} m/s",
            "rainfall": f"{rain['1h']:.1f} mm/h" if "1h" in rain else "Not reported",
            "observed_at": observed_at,
            "risk_level": assessment["level"],
            "risk_reasons": assessment["reasons"],
        }


def get_weather_report(location_name):
    """Look up one location, fetch its weather, assess it and format the result."""
    # Check both credentials before making any external requests.
    mapbox = MapboxClient()
    weather_client = WeatherClient()
    location = mapbox.geocode(location_name)
    weather = weather_client.get_weather(location["latitude"], location["longitude"])
    assessment = RiskEngine().assess(weather)
    return DataFormatter().format(location, weather, assessment)
