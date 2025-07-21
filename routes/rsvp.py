from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import RSVP
import os
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Load environment variables from .env file
load_dotenv()

security = HTTPBasic()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# Dependency to verify admin credentials
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rsvp", response_class=HTMLResponse)
async def rsvp_form(request: Request, success: str = None):
    return templates.TemplateResponse("rsvp_form.html", {
        "request": request,
        "success": success == "true",
        "dinner_confirmed": False
    })

@router.post("/rsvp", response_class=HTMLResponse)
async def submit_rsvp(request: Request, name: str = Form(...), attendance: str = Form(...), db: Session = Depends(get_db)):
    dinner_confirmed = attendance in ["dinner", "both"]
    party_confirmed = attendance in ["party", "both"]

    rsvp = RSVP(name=name, dinner_confirmed=dinner_confirmed, party_confirmed=party_confirmed)
    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)

    # Redirect to the GET route with a success query parameter
    return RedirectResponse(url="/rsvp?success=true", status_code=303)

@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(verify_admin)])
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).all()

    # Format data for the template
    formatted_rows = [
        (rsvp.name, rsvp.timestamp.strftime('%d/%m') if rsvp.timestamp else '', rsvp.dinner_confirmed, rsvp.party_confirmed)
        for rsvp in rsvps
    ]

    # Calculate totals
    total_dinner = sum(1 for rsvp in rsvps if rsvp.dinner_confirmed)
    total_party = sum(1 for rsvp in rsvps if rsvp.party_confirmed)

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "rsvps": formatted_rows,
        "total_dinner": total_dinner,
        "total_party": total_party
    })

