# Project Plan
##  Executive Summary: 
This project is all about building a dashboard for Kestrel Data, where they can just open their browser and the dashboard does the job of pulling in the live weather data, calculates risk and flags any problematic routes. Currently the logistics consultants are spending a huge portion of their time to manually check the weather and figure out if any route is probably going to be delayed. This system helps the team make faster and safer decisions about where to route their freight. 

## 1. Project Scope and Deliverables
** Target Audience:** This platform is built for the internal operations team (Deb, Priya and Marcus) to be accessed directly from their browser without needing any new software.
**Core Functionality:** The weather conditions for active freight lanes is pulled in and the risks are calculated, displaying potential delays.
**Technology Stack:**Python 3.11+, and FastAPI is used for the backend architecture while Jinja2 is used for server-side HTML templating and Pico CSS is used for lightweight frontend.
** Out of Scope:** We made a decision to drop user logins and session management due to the short timeframe we had for delivery.
**Final Deliverables:**A comprehensive handover report detailing API integration strategy, a GitHub repository containing Python and FastAPI codebase. 


##Requirements and Feature Implementation Matrix

| Requirement / User Story | Implementation Approach | Status | Notes / Scope Adjustments | 
| :---  |  :---  |  :---  |  :---  |
| **US-01: No-Install Interface**<br>*As an operator, I want to see the data in the browser, so I don’t have to install any other software.* | Jinja2 templates are used to display HTML and CSS pages through the FastAPI backend. | **Completed** |  We got a clean and professional look without any heavy frontend dependencies using PicoCSS |
 | **US-02: Live Weather Risk Data**<br>*As a logistic consultant, I want real-time weather data so I can see where delays are more likely to occur.* | Precipitation, wind and severe weather alerts are pulled through the OpenWeatherMap REST API. | **In Progress** | The API is being wrapped in an object-oriented client by the Backend lead |
| **US-03: Secondary Analytical Integration**<br>*As an analyst, I want automated risk assessments instead of just raw numbers.* | A second integration judges risk and decides how serious it is or provides traffic and road details. |**In Progress** | we chose the fixed scoring rules because they give the same answer each time and also don't have to wait for an outside service. |
| **US-04: Developer Handover and API Readiness**<br>*As Deb, I want a clean python structure and API endpoints so a commercial API can be built later.* | OpenAPI documentation at /docs created by FastAPI automatically and, Modular OOP Architecture. | **Planned** | Kestrel Plans to eventually offer endpoints to the clients so we chose FastAPI. |
| **US-05: Multi-login Client Authentication**<br>*As Marcus, I want client logins so the clients can access the system themselves* | User Management and JWT session Authentication . | **Out of Scope** | The two-week deadline is too close so was dropped and the app is currently being built for Deb's internal evaluation. |


## Division of Labour and Workflow Model
A Sequential relay model was used to prevent GitHub merge conflicts and also so each individual can choose and focus on their speciality. Each person completes their own portion and hands it off to the next person. 
Part 1: Architecture and Foundation (Days 1-3): Building Repository Architecture, structuring directory, web scaffolding and baseline project planning.
Part 2: Backend Integration and Logic (Days 4-7): Object-oriented API integrations and data binding to the UI templates in real time.
Part 3:Quality Assurance and Business Documentation (Days 8-11): End-to-end testing, user manual creation and exception handling.
Part 4: Video Pitch and Final Handover (Days 12-15): Scripting, Screen demonstrating and final handover to the client.

