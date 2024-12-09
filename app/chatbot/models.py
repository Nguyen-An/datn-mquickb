from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel

class ChatbotData(Base):
    __tablename__ = 'chatbot_data'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255))
    file_path = Column(String(255))
    key = Column(String(255))
    uploaded_at = Column(TIMESTAMP)

class CreateAssistant(BaseModel):
    name: str = None
    instructions: str = None
    model:str  = 'gpt-3.5-turbo'

class CreateUserThread(BaseModel):
    name: str = None   

class MessageThread(BaseModel):
    mes: str = ""