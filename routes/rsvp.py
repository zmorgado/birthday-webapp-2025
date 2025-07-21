from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Load environment variables from .env file
load_dotenv()

# Database setup
def init_db():
    conn = sqlite3.connect("rsvp.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rsvps (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        dinner_confirmed BOOLEAN NOT NULL,
                        party_confirmed BOOLEAN,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

init_db()

security = HTTPBasic()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# Dependency to verify admin credentials
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

@router.get("/rsvp", response_class=HTMLResponse)
async def rsvp_form(request: Request, success: str = None):
    return templates.TemplateResponse("rsvp_form.html", {
        "request": request,
        "success": success == "true",
        "dinner_confirmed": False
    })

@router.post("/rsvp", response_class=HTMLResponse)
async def submit_rsvp(request: Request, name: str = Form(...), attendance: str = Form(...)):
    dinner_confirmed = attendance in ["dinner", "both"]
    party_confirmed = attendance in ["party", "both"]

    conn = sqlite3.connect("rsvp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rsvps (name, dinner_confirmed, party_confirmed) VALUES (?, ?, ?)", (name, dinner_confirmed, party_confirmed))
    conn.commit()
    conn.close()

    # Redirect to the GET route with a success query parameter
    return RedirectResponse(url="/rsvp?success=true", status_code=303)

@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(verify_admin)])
async def admin_dashboard(request: Request):
    conn = sqlite3.connect("rsvp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, timestamp, dinner_confirmed, party_confirmed FROM rsvps")
    rows = cursor.fetchall()

    # Convert timestamp strings to datetime objects and format as day/month only
    formatted_rows = [
        (row[0], datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%d/%m') if row[1] else '', row[2], row[3])
        for row in rows
    ]

    # Calculate totals
    total_dinner = sum(1 for row in formatted_rows if row[2])
    total_party = sum(1 for row in formatted_rows if row[3])

    conn.close()

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "rsvps": formatted_rows,
        "total_dinner": total_dinner,
        "total_party": total_party
    })

