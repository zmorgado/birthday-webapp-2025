from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class RSVP(Base):
    __tablename__ = 'rsvps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    dinner_confirmed = Column(Boolean, nullable=False)
    party_confirmed = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, default='CURRENT_TIMESTAMP')

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rsvp.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
