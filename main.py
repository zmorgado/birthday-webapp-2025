from fastapi import FastAPI
from config import Config
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes import rsvp
from models import init_db
import os
import uvicorn
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database during startup
    yield  # Perform any cleanup if necessary

# Pass the lifespan handler to the FastAPI app
app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(rsvp.router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Bienvenidos a la invitación de cumpleaños</h1>"

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))  # Use PORT from environment or default to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
