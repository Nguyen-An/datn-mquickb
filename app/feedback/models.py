from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    menu_item_id = Column(Integer)
    rating = Column(Integer)
    comments = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)