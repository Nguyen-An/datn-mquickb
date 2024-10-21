from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str