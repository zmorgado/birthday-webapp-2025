from fastapi import FastAPI, Depends, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import init_db, RSVP, SessionLocal
from config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database during startup
    yield  # Perform any cleanup if necessary

# Pass the lifespan handler to the FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
origins = [
    "https://cumplepelusa.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to verify admin credentials
security = HTTPBasic()
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != Config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")

# Pydantic model for RSVP submissions
class RSVPRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Name must be non-empty")
    dinner_confirmed: bool
    party_confirmed: bool

@app.post("/rsvp")
async def submit_rsvp(rsvp: RSVPRequest, db: Session = Depends(get_db)):
    new_rsvp = RSVP(
        name=rsvp.name,
        dinner_confirmed=rsvp.dinner_confirmed,
        party_confirmed=rsvp.party_confirmed
    )
    db.add(new_rsvp)
    db.commit()
    return {"message": "RSVP submitted successfully"}

@app.get("/admin", dependencies=[Depends(verify_admin)])
async def admin_dashboard(db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).all()
    return rsvps