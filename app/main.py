from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Kestrel Data Dashboard")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    mock_data = {
        "status": "System Online - Awaiting API", 
        "message": "Welcome to the Kestrel Data prototype."
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": mock_data})