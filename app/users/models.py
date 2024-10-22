from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

# SQLAlchemy model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password_hash = Column(String(255))
    role = Column(String(20))
    phone_number = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    phone_number: str
