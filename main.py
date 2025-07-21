from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes import rsvp

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(rsvp.router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Bienvenidos a la invitación de cumpleaños</h1>"
