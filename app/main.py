"""Serve the browser dashboard and bind location searches to weather reports."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api_clients import APIError
from app.weather_analysis import get_weather_report


APP_DIRECTORY = Path(__file__).resolve().parent
load_dotenv(APP_DIRECTORY.parent / ".env")

app = FastAPI(title="Kestrel Data Dashboard")
templates = Jinja2Templates(directory=str(APP_DIRECTORY / "templates"))


@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request, location: str | None = None):
    """Show the search form, a formatted report, or a readable API error."""
    report = None
    error = None
    if location is not None:
        location = location.strip()
        if not location:
            error = "Enter a location name, such as Perth, Australia."
        else:
            try:
                report = get_weather_report(location)
            except APIError as problem:
                error = str(problem)

    # A normal function lets FastAPI run the blocking API calls in its thread pool.
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"location": location or "", "report": report, "error": error},
    )
