import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
