# Kestrel Data Weather Risk Dashboard
## Project Report & Technical Handover

**Course:** ISYS3015 — Business Application Development  
**Client:** Marcus & Priya, Kestrel Data  
**Team Members:** Amisha (Lead Architect), Faisal (Backend Integration Engineer), Jimin Lee (QA & Technical Writer)  
**Repository:** `https://github.com/amisha284/kestrel-weather-dashboard`  

---

## 1. Executive Summary & Client Context

Kestrel Data is a boutique analytics and consultancy firm founded four years ago by Marcus and Priya. Having established a steady revenue foundation (~$180,000 annually) primarily through bespoke consulting for logistics operators, Kestrel Data identified an urgent operational bottleneck: clients repeatedly request intelligence regarding weather-related disruptions along freight corridors. Historically, Priya responded to these inquiries using manually updated spreadsheets—a methodology that proved unsustainable and prevented recurring commercial scalability.

Previous attempts by Kestrel Data to engage freelance developers resulted in technical failure; contractors delivered opaque "black-box" systems that could not be maintained once the developer departed. To eliminate this issue, our team established three foundational constraints guided by the client brief:
1. **Python-Native Architecture:** Deb, Kestrel Data’s office manager, maintains internal infrastructure in Python. The delivered codebase must be completely readable and maintainable by Deb and future developers.
2. **Browser-Accessible Interface:** End-users and logistics operators refuse complex desktop installations. The solution must run natively in standard web browsers.
3. **Future API Readiness:** While currently serving internal operational needs, the architecture must support seamless expansion into a commercial data API that Kestrel Data can monetize.

The delivered prototype satisfies these directives, coupling an object-oriented Python architecture with lightweight server-rendered HTML to deliver automated weather risk evaluations.

---

## 2. Project Approach & Sequential Relay Methodology

To prevent merge conflicts and leverage individual strengths across a strict two-week delivery cycle, the team adopted a **Sequential Relay Model**. Work was divided into four discrete stages:
* **Phase 1: Architecture & Foundation (Days 1–3):** Repository initialization, virtual environment setup, directory structuring, and baseline FastAPI/Jinja2 scaffolding.
* **Phase 2: Backend Integration & Logic (Days 4–7):** Object-oriented API client development, geocoding coordinates, live weather data binding, and algorithmic risk rule evaluation.
* **Phase 3: Quality Assurance & Business Documentation (Days 8–11):** Unit and integration testing, boundary condition validation, user manual creation, and business impact modeling.
* **Phase 4: Developer Handover & Video Demonstration (Days 12–15):** Code reviews, architectural documentation, and stakeholder video walkthrough.

Team workflow was governed through a central Trello board tracking user stories (US-01 through US-05) from backlog to deployment. Code integrity was protected using GitHub branch protection rules: direct commits to `main` were disabled, requiring all functional additions to pass peer code reviews via feature pull requests.

---

## 3. Software Architecture & Technical Design

The application follows an Object-Oriented, modular architecture designed for high maintainability and low operational overhead. Rather than implementing an unnecessarily heavy JavaScript framework, the application utilizes **FastAPI** paired with **Jinja2** templates and **Pico CSS**. This server-rendered approach ensures near-instant page loads, zero client-side build dependencies, and complete code accessibility for Deb.

FastAPI handles incoming HTTP requests and binds query parameters to backend services. When an operator searches for a location, the controller calls `get_weather_report()` within `app/weather_analysis.py`, coordinating the data extraction, transformation, analysis, and presentation pipeline.

### Object-Oriented Inheritance & Encapsulation
External API communication is structured using an object-oriented hierarchy:
* **`BaseClient` (`app/api_clients.py`):** Abstract parent class that manages credential retrieval via environment variables and encapsulates HTTP communication. It implements robust error-handling conventions with 10-second request timeouts, intercepting HTTP 401, 403, 429, and 500 status codes. Secret API keys and internal query URLs are strictly masked from exceptions, preventing credential leaks in logs or UI alerts.
* **`MapboxClient` (`app/api_clients.py`):** Inherits from `BaseClient`. Converts arbitrary location queries into validated geographic coordinates using the Mapbox Geocoding v6 endpoint. It enforces input sanitization (256-character limits and semicolon removal to prevent injection attacks).
* **`WeatherClient` (`app/api_clients.py`):** Inherits from `BaseClient`. Ingests coordinate tuples and queries the OpenWeatherMap API. Payload integrity is enforced by an independent `validate_weather()` function that rigorously confirms numeric ranges, finite floating-point values, and schema conformity.

### Analytical Risk Engine & Presentation Formatting
* **`RiskEngine` (`app/weather_analysis.py`):** Decouples business logic from data ingestion. It evaluates current wind velocities, hourly rainfall, and atmospheric condition codes against established risk thresholds:
  * *High Risk:* Wind speeds ≥ 15 m/s, precipitation ≥ 7.5 mm/h, or thunderstorm codes (IDs 200–299).
  * *Medium Risk:* Wind speeds ≥ 8 m/s or precipitation ≥ 2.5 mm/h.
  * *Low Risk:* Normal operational baseline.
  The engine aggregates explanatory disruption reasons, ensuring logistics operators understand the qualitative drivers behind an alert.
* **`DataFormatter` (`app/weather_analysis.py`):** Converts validated floating-point metrics into standardized display strings with units and parses UNIX timestamps into ISO UTC formatting. Missing rainfall data safely defaults to *"Not reported"* without crashing the application.

---

## 4. Business Value & Operational Impact

The implementation of the Kestrel Data Weather Risk Dashboard delivers quantifiable operational improvements across three primary dimensions:

### Elimination of Manual Overhead
Priya’s initial market pilot proved that commercial demand exists but confirmed that manual spreadsheet maintenance was unviable. By automating coordinate resolution and weather fetching into a sub-second query, the dashboard eliminates approximately 15–20 minutes of manual data aggregation per inquiry. This enables Kestrel Data staff to handle higher inquiry volumes without increasing contractor headcount.

### Proactive Logistics Risk Mitigation
In freight logistics, unexpected transit disruptions result in severe financial penalties, missed connection windows, and deteriorated client trust. By categorizing atmospheric conditions into actionable Low, Medium, and High risk profiles with explicit operational rationales, Kestrel Data can advise logistics partners proactively—recommending route diversions or schedule buffering before cargo departs.

### Foundation for Commercial API Monetization
Marcus identified a strategic desire to eventually offer an independent API service. By constructing the backend using FastAPI, Kestrel Data is immediately equipped with automated OpenAPI schemas (`/openapi.json`) and interactive documentation (`/docs`). Exposing a JSON-based weather-risk endpoint to external commercial subscribers requires only a minor routing extension, positioning Kestrel Data for recurring SaaS revenue.

---

## 5. Quality Assurance & Reliability Verification

To guarantee that the application holds up under regular daily use by Deb and Marcus, the team executed an exhaustive quality assurance strategy comprising 17 automated test cases across three test modules:

1. **API Client & Network Mocking (`tests/test_api_clients.py`):**
   Using `unittest.mock.patch`, external network requests were simulated to verify system resilience against upstream provider failures. Tests confirm correct handling of missing credentials, coordinate boundary violations, upstream timeouts, HTTP 429 rate limits, and corrupted JSON payloads.
2. **Analytical Boundaries & Risk Logic (`tests/test_weather_analysis.py`):**
   Unit tests evaluate the decision engine against edge cases, verifying that boundary conditions (e.g., exactly 7.99 m/s vs 8.00 m/s wind) trigger appropriate risk levels, that thunderstorm overrides supersede lower risks, and that missing optional keys do not cause runtime failures.
3. **Web Dashboard & XSS Injection Protection (`tests/test_dashboard.py`):**
   Evaluates full HTTP request lifecycles using FastAPI’s `TestClient`. Confirms template variable interpolation and verifies that Jinja2 auto-escaping neutralizes script injection attacks (XSS) when untrusted location strings are submitted.

---

## 6. Implementation Changes Against Initial Project Plan

During the sprint, two deliberate scope adjustments were made:
1. **Selection of External Integrations:** The preliminary project plan contemplated integrating a specialized road traffic or freight lane API alongside weather feeds. However, investigation revealed that commercial transit APIs imposed restrictive paywalls and complex enterprise contracts. The team adjusted the scope to combine **Mapbox Geocoding** with **OpenWeatherMap**, running analytical evaluations locally. This achieved the brief's requirement of two external resources while maintaining a predictable, cost-free development footprint.
2. **Exclusion of User Authentication:** Requirement US-05 (JWT client authentication) was deferred to future work. Marcus indicated that Deb and internal staff would evaluate the prototype internally before exposing it to external clients. Dropping authentication allowed the team to allocate development effort toward error handling, test coverage, and documentation.

---

## 7. Reflective Component (400–600 Words)

### Project Lead & Architectural Reflection (Amisha)
"Managing the initial repository scaffolding and project coordination highlighted the delicate balance between architectural ambition and practical delivery. Early in the sprint, I considered proposing a decoupled single-page application utilizing React or Vue. However, examining the client brief made it obvious that Kestrel Data’s primary maintainer, Deb, is an internal Python specialist, not a frontend JavaScript engineer. Pivoting to a server-rendered FastAPI and Jinja2 stack ensured that Deb can comfortably maintain and extend every file in the repository without learning modern node toolchains. What didn’t work smoothly was our sequential relay handover model: because team members operated on isolated branches across different days, integration miscommunications occurred near the deadline where documentation diverged from live code. In future sprints, I would enforce daily synchronization standups, integrate automated continuous integration checks on pull requests, and require strict rebase validations before merging documentation branches into main."

### Backend & API Integration Reflection (Faisal)
"Designing the backend services emphasized the critical necessity of defensive programming when consuming third-party cloud APIs. External web services are inherently unpredictable: remote connections time out, rate limits expire during peak traffic, and response payloads occasionally omit optional measurements such as hourly rainfall. Implementing an abstract `BaseClient` allowed me to centralize error handling, enforce 10-second timeouts, and ensure API tokens are never leaked in client-facing exceptions or stack traces. Encapsulating the business logic within a distinct `RiskEngine` also proved highly effective, as it cleanly decoupled mathematical threshold analysis from network I/O. What proved challenging was negotiating provider rate limits during rapid automated testing cycles. If I were to approach this project again, I would implement an asynchronous HTTP client such as `httpx` to handle concurrent location queries and introduce an in-memory caching layer (such as Redis) to cache geocoded coordinates, drastically reducing external API costs and latency for repeated searches."

### Quality Assurance & Documentation Reflection (Jimin Lee)
"Leading quality assurance reinforced the lesson that automated test suites are only as reliable as the environments and code revisions against which they are integrated. Initially, I developed test cases against an early prototype shell, which caused discrepancies when integrated against Faisal's live backend. Re-aligning the test suite to validate mock API payloads, boundary conditions, and HTML escaping taught me the immense value of continuous test-driven development. Writing the user manual also underscored that technical capabilities mean little if the operational user cannot configure the system independently. Providing clear step-by-step guidance on `.env` setup and input formatting ensures Deb can deploy the software with complete confidence. What didn't work well was writing test cases in isolation without inspecting backend commits concurrently. In future projects, I would establish shared mock interfaces and contract definitions on Day 1 to ensure documentation, automated testing, and backend development remain perfectly synchronized."

---

## 8. Group Contribution Statement

The team collaboratively agrees upon the following breakdown of project contributions:

| Student Name | Student ID | Agreed Contribution | Primary Deliverables & Responsibilities |
| :--- | :--- | :---: | :--- |
| **Amisha** | 21917398 | **33.3%** | Repository initialization, project plan formulation, FastAPI scaffolding, PR reviews, merge management. |
| **Faisal** | 22133577 | **33.3%** | Mapbox & OpenWeatherMap API clients, `RiskEngine`, `DataFormatter`, unit tests, CLI script. |
| **Jimin Lee**| 21458920 | **33.3%** | Business value analysis, comprehensive QA test report, user manual, interface documentation. |

---
