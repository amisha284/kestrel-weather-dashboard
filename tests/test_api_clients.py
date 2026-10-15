"""Offline API checks: python -m unittest discover -s tests -v."""

import io
import os
import unittest
from unittest.mock import Mock, patch

import requests

from app.api_clients import APIError, MapboxClient, WeatherClient
from scripts.check_apis import main


# Invented examples with the same core structure as the providers' responses.
LOCATION_RESPONSE = {
    "features": [{
        "geometry": {"type": "Point", "coordinates": [115.86, -31.95]},
        "properties": {"full_address": "Perth, Western Australia, Australia"},
    }],
}
WEATHER_RESPONSE = {
    "main": {"temp": 22.5, "humidity": 60},
    "wind": {"speed": 4.1},
    "weather": [{"id": 800, "description": "clear sky"}],
}


class APIClientTests(unittest.TestCase):
    def setUp(self):
        credentials = patch.dict(os.environ, {
            "MAPBOX_ACCESS_TOKEN": "test-mapbox-token",
            "OPENWEATHER_API_KEY": "test-weather-key",
        })
        credentials.start()
        self.addCleanup(credentials.stop)

    @patch("app.api_clients.requests.get")
    def test_location_then_weather(self, get):
        get.side_effect = [
            Mock(json=Mock(return_value=LOCATION_RESPONSE)),
            Mock(json=Mock(return_value=WEATHER_RESPONSE)),
        ]
        location = MapboxClient().geocode("Perth, Australia")
        weather = WeatherClient().get_weather(location["latitude"], location["longitude"])

        self.assertEqual(location["latitude"], -31.95)
        self.assertEqual(location["longitude"], 115.86)
        self.assertEqual(weather, WEATHER_RESPONSE)
        first_request, second_request = get.call_args_list
        self.assertEqual(first_request.kwargs["params"]["q"], "Perth, Australia")
        self.assertEqual(first_request.kwargs["params"]["access_token"], "test-mapbox-token")
        self.assertEqual(second_request.kwargs["params"], {
            "lat": -31.95, "lon": 115.86, "appid": "test-weather-key", "units": "metric",
        })
        self.assertEqual(first_request.kwargs["timeout"], 10)
        self.assertEqual(second_request.kwargs["timeout"], 10)

    def test_missing_credentials(self):
        for client, name in (
            (MapboxClient, "MAPBOX_ACCESS_TOKEN"),
            (WeatherClient, "OPENWEATHER_API_KEY"),
        ):
            with self.subTest(name=name), patch.dict(os.environ, {name: " "}):
                with self.assertRaisesRegex(APIError, name):
                    client()

    @patch("app.api_clients.requests.get")
    def test_invalid_inputs_do_not_make_requests(self, get):
        for location in ("", "  ", None, "Perth;Australia", "x" * 257):
            with self.subTest(location=location), self.assertRaises(APIError):
                MapboxClient().geocode(location)
        for latitude, longitude in ((91, 0), (0, -181), (None, 0), (True, 0)):
            with self.subTest(latitude=latitude), self.assertRaises(APIError):
                WeatherClient().get_weather(latitude, longitude)
        get.assert_not_called()

    @patch("app.api_clients.requests.get")
    def test_unknown_location(self, get):
        get.return_value.json.return_value = {"features": []}
        with self.assertRaisesRegex(APIError, "No matching location"):
            MapboxClient().geocode("Unknown place")

    @patch("app.api_clients.requests.get")
    def test_connection_failures_hide_request_details(self, get):
        for exception, message in (
            (requests.Timeout("secret-url"), "timed out"),
            (requests.ConnectionError("secret-url"), "Could not connect"),
        ):
            get.side_effect = exception
            with self.subTest(exception=type(exception).__name__):
                with self.assertRaisesRegex(APIError, message) as caught:
                    MapboxClient().geocode("Perth")
                self.assertNotIn("secret-url", str(caught.exception))

    @patch("app.api_clients.requests.get")
    def test_http_errors_hide_credentials(self, get):
        for status, message in ((401, "credentials"), (403, "credentials"),
                                (429, "limit"), (500, "HTTP 500")):
            response = Mock(status_code=status)
            response.raise_for_status.side_effect = requests.HTTPError(
                "secret-url", response=response,
            )
            get.return_value = response
            with self.subTest(status=status):
                with self.assertRaisesRegex(APIError, message) as caught:
                    WeatherClient().get_weather(-31.95, 115.86)
                self.assertNotIn("secret-url", str(caught.exception))

    @patch("app.api_clients.requests.get")
    def test_invalid_json(self, get):
        get.return_value.json.side_effect = ValueError("not JSON")
        with self.assertRaisesRegex(APIError, "invalid JSON"):
            MapboxClient().geocode("Perth")

    @patch("app.api_clients.requests.get")
    def test_malformed_location_responses(self, get):
        payloads = [None, [], {}, {"features": {}}, {"features": [None]}, {
            "features": [{"geometry": {"coordinates": ["invalid", 0]},
                          "properties": {"full_address": "Perth"}}],
        }]
        for payload in payloads:
            get.return_value.json.return_value = payload
            with self.subTest(payload=payload), self.assertRaises(APIError):
                MapboxClient().geocode("Perth")

    @patch("app.api_clients.requests.get")
    def test_malformed_weather_responses(self, get):
        for payload in ({}, {"main": None}, {
            "main": {"temp": "invalid"}, "wind": {"speed": 1},
            "weather": [{"description": "clear sky"}],
        }, {"main": {"temp": 22}, "wind": {"speed": 1}, "weather": []}):
            get.return_value.json.return_value = payload
            with self.subTest(payload=payload), self.assertRaises(APIError):
                WeatherClient().get_weather(-31.95, 115.86)

    @patch("scripts.check_apis.load_dotenv")
    @patch("app.api_clients.requests.get")
    def test_smoke_script_success(self, get, load_env):
        get.side_effect = [
            Mock(json=Mock(return_value=LOCATION_RESPONSE)),
            Mock(json=Mock(return_value=WEATHER_RESPONSE)),
        ]
        with patch("sys.argv", ["check_apis", "Perth, Australia"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                main()
        self.assertIn("Both API checks passed.", output.getvalue())
        self.assertIn("22.5 °C", output.getvalue())
        self.assertNotIn("test-mapbox-token", output.getvalue())
        self.assertNotIn("test-weather-key", output.getvalue())

    @patch("scripts.check_apis.load_dotenv")
    @patch("app.api_clients.requests.get")
    def test_smoke_script_missing_key_exits_before_requests(self, get, load_env):
        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": ""}):
            with patch("sys.argv", ["check_apis", "Perth"]):
                with patch("sys.stderr", new_callable=io.StringIO) as output:
                    with self.assertRaises(SystemExit) as caught:
                        main()
        self.assertEqual(caught.exception.code, 1)
        self.assertIn("OPENWEATHER_API_KEY", output.getvalue())
        get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
