# Kestrel Data weather risk dashboard


A browser tool that Kestrel Data staff use to check weather-related disruption risk for a location. It supports freight and logistics planning.

The app resolves a place name to coordinates with the Mapbox Geocoding API. It then fetches current conditions from the OpenWeatherMap API. A local rule engine rates the risk as Low, Medium, or High. It also lists the reasons.

## Features

- Staff use the app in a browser. They do not install software.
- The server renders pages with FastAPI, Jinja2, and Pico CSS.
- The Mapbox and OpenWeatherMap clients inherit from `BaseClient`. `BaseClient` stores API keys in an internal attribute.
- The risk engine checks wind speed, rainfall, and thunderstorm conditions.
- Requests time out after ten seconds. The app shows a readable message for missing credentials, connection failures, rate limits, and invalid responses. Error messages do not include secret keys.
- FastAPI serves interactive API documentation at `/docs`.


## Quick start

### 1. Prerequisites

You need the following:

- Python 3.11 or later
- A [Mapbox](https://account.mapbox.com/) API key
- An [OpenWeatherMap](https://openweathermap.org/api) API key

### 2. Set up a virtual environment

```bash
git clone https://github.com/amisha284/kestrel-weather-dashboard.git
cd kestrel-weather-dashboard

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your API keys

Copy the example file:

```bash
cp .env.example .env
```

Set both keys in `.env`:

```ini
MAPBOX_ACCESS_TOKEN=pk.your_mapbox_token_here
OPENWEATHER_API_KEY=your_openweathermap_key_here
```

### 4. Start the app

```bash
python3 -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## Running tests

The tests use mocked API responses, so they run without API keys.

```bash
python3 -m unittest discover -s tests -v
```

Run this command to check both APIs for one location. It uses your real API keys.

```bash
python3 -m scripts.check_apis "Perth, Australia"
```
## Authors and credits

- Amisha was the lead architect and handled project scaffolding.
- Faisal handled backend integration and the risk engine.
- Jimin Lee handled quality assurance and technical documentation.
