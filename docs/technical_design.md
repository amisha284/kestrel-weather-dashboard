# Technical Design

## Setup

Use Python 3.11+ and run from the repository root:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, use `venv\Scripts\activate` and `copy .env.example .env`.
Add `MAPBOX_ACCESS_TOKEN` and `OPENWEATHER_API_KEY` to `.env`, then start:

```bash
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` and search for a location, such as
`Perth, Australia`. Keys stay on the server; `.env` is ignored by Git.
Environment variables take precedence. Restart after changing credentials.

## Backend flow

`Location → MapboxClient → WeatherClient → RiskEngine → DataFormatter → Jinja2`

FastAPI handles the search. Mapbox finds coordinates; OpenWeatherMap supplies
current conditions. Both clients inherit request handling from `BaseClient`,
which keeps credentials in an internal attribute. `get_weather_report()`
coordinates the flow, while `validate_weather()` checks required fields.
Jinja2 escapes displayed text and Pico CSS provides the layout.

## Endpoints

All endpoints use GET.

| Endpoint | Purpose / parameters |
| --- | --- |
| `/` | Optional `location` query; returns the HTML form, report or error. |
| `/docs` | Interactive application documentation. |
| `/openapi.json` | Application schema. |
| `https://api.mapbox.com/search/geocode/v6/forward` | `q`, `access_token`, `limit=1`, `autocomplete=false`. |
| `https://api.openweathermap.org/data/2.5/weather` | `lat`, `lon`, `appid`, `units=metric`. |

Mapbox returns longitude before latitude; the client converts these to named
fields. The first location match is used. There is no separate JSON weather route.

## Assessment and display

| Factor | Medium | High |
| --- | --- | --- |
| Wind | ≥8 and <15 m/s | ≥15 m/s |
| Rainfall | ≥2.5 and <7.5 mm/h | ≥7.5 mm/h |
| Thunderstorm | — | Condition code 200–299 |

The highest triggered level wins; otherwise the result is Low. Reasons explain
triggered factors. These are prototype assumptions for one location, not delay
predictions or route-wide analysis.

Measurements show units and one decimal place. Missing rainfall contributes zero
to scoring but displays “Not reported”. Observation time uses the provider's
UTC timestamp; missing time displays “Unavailable”.

## Errors and checks

Requests time out after ten seconds. `APIError` handles credentials, connection
failures, request limits and invalid responses without exposing secret URLs.
The dashboard retains the search text and displays the message.

```bash
python -m unittest discover -s tests -v
python -m scripts.check_apis "Perth, Australia"
```

Offline tests mock providers. Live checks need valid credentials. In the browser,
check the initial page, a successful search, an unknown location and missing keys.
