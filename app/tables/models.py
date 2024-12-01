from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(50))
    qr_code = Column(String(255))
    order_id = Column(Integer, default=None)
    status = Column(String(20), default='available')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class TableCreate(BaseModel):
    table_name: str
    qr_code: str
    status: str

class TableUpdate(BaseModel):
    table_name: str
    qr_code: str
    status: str
    