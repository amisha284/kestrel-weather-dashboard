"""Two focused checks for dashboard rendering and error messages."""

import unittest
from unittest.mock import patch

from fastapi import Request

from app.api_clients import APIError
from app.main import read_dashboard


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})

    @patch("app.main.get_weather_report")
    def test_search_displays_report_and_escapes_text(self, get_report):
        get_report.return_value = {
            "location": "Perth, Australia", "latitude": -31.95, "longitude": 115.86,
            "conditions": "clear sky", "temperature": "22.5 °C", "wind_speed": "8.0 m/s",
            "rainfall": "Not reported", "observed_at": "Unavailable", "risk_level": "Medium",
            "risk_reasons": ["Elevated wind speed (8.0 m/s)."],
        }
        response = read_dashboard(self.request, "  Perth, Australia  ")
        html = response.body.decode()
        get_report.assert_called_once_with("Perth, Australia")
        self.assertEqual(response.status_code, 200)
        for text in ("Perth, Australia", "22.5 °C", "8.0 m/s", "Not reported",
                     "Unavailable", "Weather risk: Medium", "Elevated wind speed"):
            self.assertIn(text, html)

        get_report.return_value["location"] = "<script>alert(1)</script>"
        html = read_dashboard(self.request, '<script>alert(1)</script>').body.decode()
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    @patch("app.main.get_weather_report")
    def test_initial_blank_and_failed_searches(self, get_report):
        html = read_dashboard(self.request).body.decode()
        self.assertIn("Enter a location above", html)
        html = read_dashboard(self.request, "  ").body.decode()
        self.assertIn("Enter a location name", html)
        get_report.assert_not_called()

        for message in (
            "No matching location was found. Try adding a country name.",
            "Set OPENWEATHER_API_KEY in your environment or .env file.",
            "The API request timed out. Please try again.",
        ):
            get_report.side_effect = APIError(message)
            with self.subTest(message=message):
                html = read_dashboard(self.request, "Perth").body.decode()
                self.assertIn('role="alert"', html)
                self.assertIn(message, html)
                self.assertNotIn("Weather risk:", html)


if __name__ == "__main__":
    unittest.main()
