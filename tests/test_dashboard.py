

import unittest
from unittest.mock import patch
from fastapi import Request
from fastapi.testclient import TestClient

from app.api_clients import APIError
from app.main import app, read_dashboard

client = TestClient(app)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})

    @patch("app.main.get_weather_report")
    def test_search_displays_report_and_escapes_text(self, get_report):
        get_report.return_value = {
            "location": "Perth, Australia",
            "latitude": -31.95,
            "longitude": 115.86,
            "conditions": "clear sky",
            "temperature": "22.5 °C",
            "wind_speed": "8.0 m/s",
            "rainfall": "Not reported",
            "observed_at": "Unavailable",
            "risk_level": "Medium",
            "risk_reasons": ["Elevated wind speed (8.0 m/s)."],
        }
        response = read_dashboard(self.request, "  Perth, Australia  ")
        html = response.body.decode()
        get_report.assert_called_once_with("Perth, Australia")
        self.assertEqual(response.status_code, 200)
        for text in (
            "Perth, Australia",
            "22.5 °C",
            "8.0 m/s",
            "Not reported",
            "Unavailable",
            "Weather risk: Medium",
            "Elevated wind speed",
        ):
            self.assertIn(text, html)


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



def test_homepage_status_code():
    """TC01: Homepage should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_dashboard_title():
    """TC02: Dashboard should display brand title."""
    response = client.get("/")
    assert "Kestrel Data Dashboard" in response.text


def test_search_form_present():
    """TC03: Search input form and button should be rendered."""
    response = client.get("/")
    assert 'name="location"' in response.text
    assert "Check weather" in response.text


def test_initial_prompt_displayed():
    """TC04: Initial state prompts user to enter location."""
    response = client.get("/")
    assert "Enter a location above to load its current weather report." in response.text


def test_invalid_route():
    """TC05: Invalid routes should return HTTP 404."""
    response = client.get("/invalid-page-does-not-exist")
    assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()