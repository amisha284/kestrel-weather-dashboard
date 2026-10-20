# Kestrel Data Weather Risk Dashboard — Quality Assurance Report

**Version:** 1.0 (Final)  
**Test Suite:** Unit, Integration, and Regression Tests  
**Test Frameworks:** Python `unittest`, `unittest.mock`, `FastAPI TestClient`, `pytest`  
**Overall Status:** **17 Passed / 0 Failed (100% Pass Rate)**  

---

## 1. Test Strategy & Scope

Testing verified system reliability across three core tiers:
1. **Network Resilience & External APIs:** Validating upstream timeouts, HTTP error codes, authentication failures, and data schema corruption without requiring active API keys (mocked via `unittest.mock`).
2. **Business Risk Decision Logic:** Validating that threshold boundaries for wind, rainfall, and thunderstorm condition codes trigger appropriate risk levels.
3. **User Interface & Web Security:** Validating route responses, HTML rendering, empty search handling, and XSS sanitization.

---

## 2. Test Execution Matrix

| Test ID | Test Category | Target Function / Module | Test Description | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC01** | UI Integration | `GET /` | Homepage route status check | HTTP 200 OK | **PASSED** |
| **TC02** | UI Integration | `dashboard.html` | Application title display | Title rendered | **PASSED** |
| **TC03** | UI Integration | `dashboard.html` | Search input form rendering | Form and button present | **PASSED** |
| **TC04** | UI Integration | `dashboard.html` | Empty search state display | Initial prompt visible | **PASSED** |
| **TC05** | Routing | `/invalid-page` | Non-existent route handler | HTTP 404 Not Found | **PASSED** |
| **TC06** | UI Integration | `read_dashboard()` | Location search report display | Formatted report rendered | **PASSED** |
| **TC07** | UI Security | `read_dashboard()` | XSS script injection test | Script tags escaped to `&lt;script&gt;` | **PASSED** |
| **TC08** | UI Error Handling | `read_dashboard()` | Whitespace-only search input | Prompt to enter location | **PASSED** |
| **TC09** | API CLI Tool | `scripts.check_apis` | CLI runner formatted output | Formatted terminal output | **PASSED** |
| **TC10** | API Resilience | `BaseClient` | Missing API credentials | `APIError` raised with setup guidance | **PASSED** |
| **TC11** | API Resilience | `MapboxClient` | Unknown location or blank query | `APIError` raised without crashing | **PASSED** |
| **TC12** | API Resilience | `WeatherClient` | Out-of-bounds coordinates (lat > 90) | `APIError` bounds rejection | **PASSED** |
| **TC13** | API Resilience | `BaseClient` | Upstream network timeout (>10s) | `APIError` timeout message | **PASSED** |
| **TC14** | API Resilience | `BaseClient` | HTTP 401, 429, 500 error responses | Human-readable error without URL leak | **PASSED** |
| **TC15** | Logic & Risk | `RiskEngine.assess` | Wind speed boundary checks (8, 15 m/s) | Correct Low/Med/High assignment | **PASSED** |
| **TC16** | Logic & Risk | `RiskEngine.assess` | Rainfall boundary checks (2.5, 7.5 mm/h) | Correct Low/Med/High assignment | **PASSED** |
| **TC17** | Logic & Risk | `RiskEngine.assess` | Thunderstorm weather condition codes | Overrides to High Risk | **PASSED** |
| **TC18** | Data Formatting | `DataFormatter.format`| Timestamp and metric formatting | Clean strings in °C, m/s, and UTC | **PASSED** |
| **TC19** | Data Formatting | `DataFormatter.format`| Missing optional rainfall payload | Defaults safely to "Not reported" | **PASSED** |
| **TC20** | Data Validation | `validate_weather` | Missing or invalid essential data | Rejects non-finite/negative values | **PASSED** |

---

## 3. Command-Line Reproduction

To verify all test cases locally:
```bash
PYTHONPATH=. ./venv/bin/pytest -v
```

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0 -- /Users/amishagautam/kestrel-weather-dashboard/venv/bin/python3.14
rootdir: /Users/amishagautam/kestrel-weather-dashboard
plugins: anyio-4.15.1
collecting ... collected 17 items

tests/test_api_clients.py::APIClientTests::test_complete_report_in_command_line PASSED [  5%]
tests/test_api_clients.py::APIClientTests::test_invalid_api_responses PASSED [ 11%]
tests/test_api_clients.py::APIClientTests::test_invalid_inputs_and_unknown_location PASSED [ 17%]
tests/test_api_clients.py::APIClientTests::test_missing_credentials PASSED [ 23%]
tests/test_api_clients.py::APIClientTests::test_timeout_and_http_errors PASSED [ 29%]
tests/test_dashboard.py::DashboardTests::test_initial_blank_and_failed_searches PASSED [ 35%]
tests/test_dashboard.py::DashboardTests::test_search_displays_report_and_escapes_text PASSED [ 41%]
tests/test_dashboard.py::test_homepage_status_code PASSED                [ 47%]
tests/test_dashboard.py::test_dashboard_title PASSED                     [ 52%]
tests/test_dashboard.py::test_search_form_present PASSED                 [ 58%]
tests/test_dashboard.py::test_initial_prompt_displayed PASSED            [ 64%]
tests/test_dashboard.py::test_invalid_route PASSED                       [ 70%]
tests/test_weather_analysis.py::WeatherAnalysisTests::test_formatted_report_has_units_and_utc_time PASSED [ 76%]
tests/test_weather_analysis.py::WeatherAnalysisTests::test_invalid_essential_weather_data PASSED [ 82%]
tests/test_weather_analysis.py::WeatherAnalysisTests::test_missing_optional_data_and_reported_zero_rainfall PASSED [ 88%]
tests/test_weather_analysis.py::WeatherAnalysisTests::test_thresholds_and_highest_level_wins PASSED [ 94%]
tests/test_weather_analysis.py::WeatherAnalysisTests::test_thunderstorm_and_combined_reasons PASSED [100%]

============== 17 passed, 1 warning, 23 subtests passed in 0.42s ===============
```

All tests pass with a 100% success rate under automated test conditions.