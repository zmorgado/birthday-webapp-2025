from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime, timezone  # Import timezone for UTC-aware datetime
from config import Config  # Import the centralized Config class

Base = declarative_base()

class RSVP(Base):
    __tablename__ = 'rsvps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    dinner_confirmed = Column(Boolean, nullable=False)
    party_confirmed = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

# Database setup
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)