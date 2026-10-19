"""Five focused checks for the coursework risk rules and display values."""

import unittest

from app.api_clients import APIError
from app.weather_analysis import DataFormatter, RiskEngine


LOCATION = {"name": "Perth, Australia", "latitude": -31.95, "longitude": 115.86}


def make_weather(wind=4.1, rain=None):
    """Build a fresh, invented payload for each test."""
    weather = {
        "main": {"temp": 22.56},
        "wind": {"speed": wind},
        "weather": [{"id": 800, "description": "clear sky"}],
        "dt": 1704067200,
    }
    if rain is not None:
        weather["rain"] = {"1h": rain}
    return weather


class WeatherAnalysisTests(unittest.TestCase):
    def test_thresholds_and_highest_level_wins(self):
        cases = [
            (0, 0, "Low"), (7.99, 0, "Low"),
            (8, 0, "Medium"), (14.99, 0, "Medium"), (15, 0, "High"),
            (0, 2.49, "Low"), (0, 2.5, "Medium"),
            (0, 7.49, "Medium"), (0, 7.5, "High"),
            (8, 2.5, "Medium"), (15, 2.5, "High"), (8, 7.5, "High"),
        ]
        for wind, rain, expected in cases:
            with self.subTest(wind=wind, rain=rain):
                result = RiskEngine().assess(make_weather(wind, rain))
                self.assertEqual(result["level"], expected)
                self.assertTrue(result["reasons"])

    def test_thunderstorm_and_combined_reasons(self):
        weather = make_weather()
        # Check that a secondary condition is also assessed.
        weather["weather"].append({"id": 201, "description": "thunderstorm"})
        result = RiskEngine().assess(weather)
        self.assertEqual(result["level"], "High")
        self.assertIn("Thunderstorm conditions reported.", result["reasons"])

        weather["wind"]["speed"] = 15
        weather["rain"] = {"1h": 7.5}
        self.assertEqual(len(RiskEngine().assess(weather)["reasons"]), 3)

    def test_formatted_report_has_units_and_utc_time(self):
        weather = make_weather(wind=8, rain=2.56)
        report = DataFormatter().format(LOCATION, weather, RiskEngine().assess(weather))
        self.assertEqual(report["location"], "Perth, Australia")
        self.assertEqual(report["temperature"], "22.6 °C")
        self.assertEqual(report["wind_speed"], "8.0 m/s")
        self.assertEqual(report["rainfall"], "2.6 mm/h")
        self.assertEqual(report["observed_at"], "2024-01-01 00:00 UTC")
        self.assertEqual(report["risk_level"], "Medium")

    def test_missing_optional_data_and_reported_zero_rainfall(self):
        weather = make_weather()
        del weather["dt"]
        assessment = RiskEngine().assess(weather)
        report = DataFormatter().format(LOCATION, weather, assessment)
        self.assertEqual(assessment, {
            "level": "Low", "reasons": ["No configured risk thresholds exceeded."],
        })
        self.assertEqual(report["rainfall"], "Not reported")
        self.assertEqual(report["observed_at"], "Unavailable")

        weather["rain"] = {"1h": 0}
        report = DataFormatter().format(LOCATION, weather, assessment)
        self.assertEqual(report["rainfall"], "0.0 mm/h")

    def test_invalid_essential_weather_data(self):
        for weather in ({}, make_weather(wind=-1), make_weather(rain="heavy")):
            with self.subTest(weather=weather):
                with self.assertRaisesRegex(APIError, "invalid weather data"):
                    RiskEngine().assess(weather)


if __name__ == "__main__":
    unittest.main()
