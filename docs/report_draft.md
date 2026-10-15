## Introduction and Client Context
Kestrel Data is a small-scale logistics consultancy that advises their clients who are logistic businesses on the weather patterns and which routes are at a risk of delay. At the moment they are doing everything manually. They gather information and analyse it by hand and write up their findings which is an extremely slow and hard-to-scale process. They requested a prototype from us that pulls live weather data, and risk scores it so the consultants can see how the weather conditions like rain, wind, or severe weather might impact freight lanes and cause delays. Their long-term goal includes providing an API to the client so they could eventually access by themselves instead of waiting for the report. We also had to ensure the codebase is completely transparent so Deb, their internal operations lead, can maintain it. We chose modular Python and FastAPI as it aligns with their future goal of offering a standalone commercial API.

## Project Approach and Team Dynamics
We only had two weeks to complete this project, so instead of relying on daily meetings, we worked on our own with each person completing a milestone and the next person continuing the work. We studied their needs and turned their requirements into Trello cards we could follow to ensure we knew what comes up next and what to build. We also used GitHub to keep the code intact during handovers, and since we had the main branch protected no one could accidentally break the working app while it was their turn.

## Preliminary Reflections and Learning Insights
In the beginning, I assumed we would need to build a complex frontend using JavaScript, but after studying the needs of Kestrel, I realised it was more important to ensure their own staff can maintain the system. Using Python and server-built web pages made setting up and running the app a much smoother process. My biggest learning through this project as the Architect was to ensure the folders are tidy, codes are clear and keeping them separate mattered more than bulking up on features, and it takes much more dedication and discipline to maintain. 


 
