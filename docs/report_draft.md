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

Initially, I expected a complex JavaScript frontend. Using Python and
server-rendered pages showed me that maintainability mattered more than extra
features. Clear folders, small classes and readable code also made handovers
easier. Future work should validate the risk thresholds against operational data
before expanding the functionality.
