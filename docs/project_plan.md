
# Project Plan
##  Executive Summary: 
This project builds a browser dashboard for Kestrel Data to search a location, retrieve current weather, and view a simple weather-risk assessment. It reduces the need to gather and format weather information manually. The delivered prototype assesses a single location; route-wide analysis and predictions of freight delays remain outside this version.

## 1. Project Scope and Deliverables
** Target Audience:** This platform is built for the internal operations team (Deb, Priya and Marcus) to be accessed directly from their browser without needing any new software.
**Core Functionality:** Mapbox resolves a searched location, OpenWeatherMap supplies current conditions, and local Python rules return Low, Medium or High risk with readable reasons.
**Technology Stack:**Python 3.11+, and FastAPI is used for the backend architecture while Jinja2 is used for server-side HTML templating and Pico CSS is used for lightweight frontend.
** Out of Scope:** We made a decision to drop user logins and session management due to the short timeframe we had for delivery.
**Final Deliverables:**A comprehensive handover report detailing API integration strategy, a GitHub repository containing Python and FastAPI codebase. 


##Requirements and Feature Implementation Matrix

| Requirement / User Story | Implementation Approach | Status | Notes / Scope Adjustments | 
| :---  |  :---  |  :---  |  :---  |
| **US-01: No-Install Interface**<br>*As an operator, I want to see the data in the browser, so I don’t have to install any other software.* | Jinja2 templates are used to display HTML and CSS pages through the FastAPI backend. | **Completed** |  We got a clean and professional look without any heavy frontend dependencies using PicoCSS |
| **US-02: Live Weather Risk Data**<br>*As a logistics consultant, I want current weather for a location so I can identify potential disruption factors.* | An object-oriented OpenWeatherMap client provides conditions, temperature, wind and available rainfall for the dashboard. | **Implemented; live validation pending** | Offline checks use mocked responses. Real provider validation requires configured credentials. Official severe-weather alerts are not included. |
| **US-03: Second External Integration and Analysis**<br>*As an analyst, I want to search a location and see a readable assessment instead of raw numbers alone.* | Mapbox Geocoding supplies coordinates as the second external integration. Local `RiskEngine` rules produce Low, Medium or High with reasons. | **Implemented; live validation pending** | Local calculations are not counted as an external integration. The fixed thresholds are prototype assumptions. |
| **US-04: Developer Handover and API Readiness**<br>*As Deb, I want a clear Python structure and endpoint documentation so another developer can continue the work.* | Modular clients, risk and formatting classes, an architecture report section, and setup/endpoint documentation under `docs/`. FastAPI generates `/docs` for the HTML route. | **Implemented for prototype** | A separate commercial JSON weather endpoint remains future work. |
| **US-05: Multi-login Client Authentication**<br>*As Marcus, I want client logins so the clients can access the system themselves* | User Management and JWT session Authentication . | **Out of Scope** | The two-week deadline is too close so was dropped and the app is currently being built for Deb's internal evaluation. |


## Division of Labour and Workflow Model
A Sequential relay model was used to prevent GitHub merge conflicts and also so each individual can choose and focus on their speciality. Each person completes their own portion and hands it off to the next person. 
Part 1: Architecture and Foundation (Days 1-3): Building Repository Architecture, structuring directory, web scaffolding and baseline project planning.
Part 2: Backend Integration and Logic (Days 4-7): Object-oriented API integrations and data binding to the UI templates in real time.
Part 3:Quality Assurance and Business Documentation (Days 8-11): End-to-end testing, user manual creation and exception handling.
Part 4: Video Pitch and Final Handover (Days 12-15): Scripting, Screen demonstrating and final handover to the client.

## Implementation Changes Against the Plan

The initial plan suggested a second analytical or road-data service. The implemented
choice uses Mapbox for location lookup and OpenWeatherMap for current weather, with
local rules for analysis. This provides two external resources and keeps the
assessment predictable and straightforward to explain and maintain.

The initial description also referred to freight lanes and predicted delays.
The delivered prototype searches one location and shows current weather with a
qualitative assessment. Route-wide analysis and measured delay predictions need
additional data and validation, so they remain future work. Browser binding and
offline checks are implemented; live provider checks still require credentials.

