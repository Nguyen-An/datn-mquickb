from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    table_id = Column(Integer)
    total_amount = Column(BigInteger)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    menu_item_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(String(20))
    price = Column(BigInteger)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class StaffCall(Base):
    __tablename__ = 'staff_calls'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer)
    reason = Column(Text)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20))

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    status: str


class listOrderItemCreate(BaseModel):
    order_id: Optional[int] 
    items: List[OrderItemCreate]
    
class StaffCallCreate(BaseModel):
    table_id: int
    reason: str