from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text)

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class UserLogin(BaseModel):
    email: str
    password: str

class TokenData():
    def __init__(self, id, user_name, email, company_id, company_name, phone_number, role_id):
        self.id = id  
        self.user_name = user_name  
        self.email = email  
        self.company_id = company_id  
        self.company_name = company_name  
        self.phone_number = phone_number  
        self.role_id = role_id  

class Test(BaseModel):
    text: str
