from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_homepage_status_code():
    """TC01: Homepage should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_dashboard_title():
    """TC02: Dashboard should display its title."""
    response = client.get("/")
    assert "Kestrel Data Dashboard" in response.text


def test_system_status():
    """TC03: Dashboard should display system status."""
    response = client.get("/")
    assert "System Online" in response.text


def test_weather_analysis_section():
    """TC04: Weather analysis section should exist."""
    response = client.get("/")
    assert "Weather Risk Analysis" in response.text


def test_invalid_route():
    """TC05: Invalid routes should return HTTP 404."""
    response = client.get("/invalid-page")
    assert response.status_code == 404