
## Introduction and Client Context

Kestrel Data needs a browser application that reduces manual weather checks and
helps staff identify potential disruption factors. The prototype searches one
location and displays current weather with a simple risk assessment. Python
supports the client's maintenance needs, while a commercial API remains a future
possibility.

## Project Approach and Team Dynamics

The team divided work into foundation, integration, testing and handover stages.
Trello tracked requirements and progress, while GitHub supported version control
and developer handovers. Protected branches require changes to pass through a
pull request before entering the main branch.

## Software Architecture and Technical Design

FastAPI handles location searches, Jinja2 renders HTML, and Pico CSS provides the
layout. The GET search form calls `get_weather_report()`, which coordinates the
backend without a separate JavaScript application.

`MapboxClient` converts a location name into coordinates. `WeatherClient` uses
these coordinates to retrieve current conditions from OpenWeatherMap. These are
the two external integrations; risk calculations run locally.

Both clients inherit request handling from `BaseClient`. Its internal credential
attribute demonstrates Python's encapsulation convention. Shared validation
checks required weather fields, while each class has a clear responsibility.

`RiskEngine` applies wind, rainfall and thunderstorm thresholds, returning Low,
Medium or High with reasons. The highest triggered level wins. These are
prototype assumptions rather than validated predictions of freight delays.
`DataFormatter` adds units and formats observation time in UTC. Missing rainfall
displays “Not reported”; missing timestamps display “Unavailable”.

Credentials come from environment variables or an ignored `.env` file. Requests
have ten-second timeouts, and `APIError` produces readable messages without
exposing keys. Jinja2 escapes displayed text. Focused tests use mocked responses
to check API handling, risk boundaries, formatting and dashboard behaviour.
Live provider verification requires configured credentials. Setup and endpoint
details are documented separately; login systems and route-wide analysis remain
outside this prototype.

## Preliminary Reflections and Learning Insights

In the beginning, I assumed we would need to build a complex frontend using JavaScript, but after studying the needs of Kestrel, I realised it was more important to ensure their own staff can maintain the system. Using Python and server-built web pages made setting up and running the app a much smoother process. My biggest learning through this project as the Architect was to ensure the folders are tidy, codes are clear and keeping them separate mattered more than bulking up on features and it takes much more dedication and discipline to maintain

## Technical Design and Implementation

### Application Architecture

The Kestrel Data Weather Dashboard is being developed as a Python-based web application using the FastAPI framework. The current prototype follows a server-rendered architecture, with FastAPI handling HTTP requests and Jinja2 templates generating the HTML interface. This approach provides a relatively lightweight foundation for a browser-accessible application.

The project separates the main application logic in `app/main.py` from the presentation layer in `app/templates/dashboard.html`. This separation is intended to improve code readability and make future modifications easier for developers and Kestrel Data staff.

### Current Implementation

The application currently provides a homepage route that returns an HTML dashboard. The FastAPI endpoint passes a dictionary containing system status information and a welcome message to the Jinja2 template. The dashboard displays these values alongside a placeholder for the planned Weather Risk Analysis functionality.

The initial application was successfully launched using Uvicorn, and the homepage returned an HTTP 200 response. Automated tests also confirmed that the expected interface components were displayed and invalid routes returned HTTP 404 responses.

### Planned External Integrations

The next development stage involves connecting the dashboard to two external data sources, as required by the project brief. These integrations are intended to replace the current mock data with live information and support weather-related analysis.

The completed application will also require appropriate error handling for unavailable services, invalid responses and network failures. Keeping external data retrieval separate from the presentation layer would support maintainability and future extension.

At the current stage, these integration features remain planned rather than implemented in the reviewed main branch.

### Maintainability and Future Development

The existing project structure provides a foundation for further development. As functionality expands, separating external API communication, data processing and user interface components into dedicated modules would improve maintainability.

Further testing will be necessary after integration to verify data accuracy, application reliability and the usability of the completed dashboard.


## Business Value and Expected Benefits

### Improved Decision-Making

The proposed Kestrel Data Weather Dashboard aims to improve business decision-making by providing users with a centralised platform for accessing weather information and risk analysis. By integrating external data sources into a browser-based application, the solution is intended to reduce the need to consult multiple websites or manually interpret weather information. This could help users identify potentially disruptive weather conditions and make more informed operational decisions.

### Operational Efficiency

A key expected benefit of the dashboard is improved operational efficiency. Automated retrieval and presentation of weather data could reduce repetitive manual tasks and allow staff to focus on interpreting information rather than collecting it. The planned use of Python, FastAPI and modular software components also supports a more structured development approach. Clear separation between application logic, external integrations and the user interface may simplify maintenance and future improvements.

### Accessibility and User Experience

The dashboard is designed to provide an accessible browser-based interface for users with different levels of technical experience. This is particularly important for Kestrel Data because the solution should remain understandable and manageable after the development team completes the project. A clear interface, supporting user documentation and appropriate error messages can reduce the learning effort required for new users.

The planned user manual will provide step-by-step instructions for accessing the application, understanding dashboard outputs and troubleshooting common issues. These resources are expected to improve user independence and reduce reliance on the original developers.

### Long-Term Business Value

The proposed application also offers potential long-term value through its modular architecture and integration capabilities. A well-structured Python codebase can support the addition of new external data services, analytical features and visualisations as business requirements evolve. Automated testing and documented development processes can further improve reliability and make future modifications easier to manage.

However, these benefits depend on successful API integration, accurate data processing, appropriate error handling and satisfactory testing. At the current prototype stage, the application demonstrates the basic web interface, while the operational benefits remain anticipated rather than verified.

Overall, the Kestrel Data Weather Dashboard is intended to deliver a more efficient, accessible and maintainable approach to weather-related information and risk assessment. Its business value will be strengthened by completing the external integrations, validating the accuracy of the displayed information and providing clear documentation for future users and maintainers.


## Testing and Quality Assurance

Quality assurance was conducted to evaluate the functionality and reliability of the Kestrel Data Weather Dashboard prototype. Automated testing was implemented using Pytest and FastAPI TestClient to verify the application's core web functionality.

Five automated test cases were executed, covering successful homepage access, dashboard title rendering, system status display, the presence of the Weather Risk Analysis section, and invalid route handling. All five tests passed successfully, achieving a 100% pass rate for the initial test suite.

The application was also launched locally using Uvicorn, and the homepage successfully returned an HTTP 200 response. Visual inspection confirmed that the dashboard displayed the expected system status and weather analysis placeholder.

Testing activities were documented in a QA Test Report to support traceability and future maintenance. However, the current tests only validate the initial prototype. Additional testing is required once the external API integrations are completed, including invalid inputs, API connection failures, network timeouts, missing data, and the accuracy of weather-related outputs.

Overall, the initial testing established a baseline for application functionality. Further integration and end-to-end testing will be necessary to confirm that the completed dashboard meets Kestrel Data's requirements.

### Quality Assurance and Collaboration Reflection

From a quality assurance perspective, the project highlighted the importance of testing throughout development rather than treating it as a final activity. Creating automated tests using Pytest and FastAPI TestClient helped establish a structured approach to verifying the dashboard's core functionality. The initial five tests passed, confirming that the prototype displayed its expected interface components and handled invalid routes correctly.

Working with GitHub also provided valuable experience in collaborative software development. The protected main branch required changes to be submitted through pull requests, reinforcing the importance of code reviews and controlled integration. This process demonstrated how version control can support accountability and reduce the risk of unreviewed changes affecting shared code.

Preparing the user manual highlighted another important lesson: technical functionality alone does not guarantee that an application is useful. Clear instructions and accessible documentation are essential, particularly when the client intends to maintain the system independently.

A limitation of the initial testing was that the external APIs had not yet been integrated into the prototype being tested. Consequently, the tests could not verify live weather data or integration reliability. This demonstrated the importance of distinguishing between successful prototype testing and validation of the completed system. In future projects, earlier integration testing and more comprehensive error-handling scenarios would help identify issues sooner.

