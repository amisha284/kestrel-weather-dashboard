"""Five focused API checks using invented responses instead of live requests."""

import io
import os
import unittest
from unittest.mock import Mock, patch

import requests

from app.api_clients import APIError, MapboxClient, WeatherClient
from scripts.check_apis import main


class APIClientTests(unittest.TestCase):
    def setUp(self):
        credentials = patch.dict(os.environ, {
            "MAPBOX_ACCESS_TOKEN": "test-token",
            "OPENWEATHER_API_KEY": "test-key",
        })
        credentials.start()
        self.addCleanup(credentials.stop)

    @patch("scripts.check_apis.load_dotenv")
    @patch("app.api_clients.requests.get")
    def test_complete_report_in_command_line(self, get, load_env):
        get.side_effect = [
            Mock(json=Mock(return_value={"features": [{
                "geometry": {"coordinates": [115.86, -31.95]},
                "properties": {"full_address": "Perth, Australia"},
            }]})),
            Mock(json=Mock(return_value={
                "main": {"temp": 22.5}, "wind": {"speed": 4.1},
                "weather": [{"id": 800, "description": "clear sky"}],
            })),
        ]
        with patch("sys.argv", ["check_apis", "Perth, Australia"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                main()
        self.assertIn("Perth, Australia", output.getvalue())
        self.assertIn("22.5 °C", output.getvalue())
        self.assertIn("Risk level: Low", output.getvalue())
        self.assertIn("Both API checks passed.", output.getvalue())
        self.assertNotIn("test-token", output.getvalue())
        self.assertNotIn("test-key", output.getvalue())
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args.kwargs["params"], {
            "lat": -31.95, "lon": 115.86, "appid": "test-key", "units": "metric",
        })

    def test_missing_credentials(self):
        for client, name in (
            (MapboxClient, "MAPBOX_ACCESS_TOKEN"),
            (WeatherClient, "OPENWEATHER_API_KEY"),
        ):
            with self.subTest(name=name), patch.dict(os.environ, {name: ""}):
                with self.assertRaisesRegex(APIError, name):
                    client()

    @patch("app.api_clients.requests.get")
    def test_invalid_inputs_and_unknown_location(self, get):
        with self.assertRaises(APIError):
            MapboxClient().geocode("")
        with self.assertRaises(APIError):
            WeatherClient().get_weather(91, 0)
        get.assert_not_called()

        get.return_value.json.return_value = {"features": []}
        with self.assertRaisesRegex(APIError, "No matching location"):
            MapboxClient().geocode("Unknown place")

    @patch("app.api_clients.requests.get")
    def test_timeout_and_http_errors(self, get):
        get.side_effect = requests.Timeout()
        with self.assertRaisesRegex(APIError, "timed out"):
            MapboxClient().geocode("Perth")

        get.side_effect = None
        for status, message in ((401, "credentials"), (429, "limit"), (500, "HTTP 500")):
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
    def test_invalid_api_responses(self, get):
        get.return_value.json.side_effect = ValueError("not JSON")
        with self.assertRaisesRegex(APIError, "invalid JSON"):
            MapboxClient().geocode("Perth")

        get.return_value.json.side_effect = None
        get.return_value.json.return_value = {}
        with self.assertRaisesRegex(APIError, "invalid weather data"):
            WeatherClient().get_weather(-31.95, 115.86)


if __name__ == "__main__":
    unittest.main()
