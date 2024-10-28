from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime
from sqlalchemy import desc

def create_order_item_db(db: Session, orderItem: OrderItem):
    db.add(orderItem)
    db.commit()
    db.refresh(orderItem)
    return orderItem

def get_order_db(db: Session,order_id, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
        limit = 9999999999
    

    if order_id is None:
        items = db.query(OrderItem).offset(offset).limit(limit).all()
        total = db.query(OrderItem).count()
    else:
        items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        total = db.query(OrderItem).filter(OrderItem.order_id == order_id).count()

    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }


def get_order_id_by_user_id(db: Session, user_id: int):
    item = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).first()
    return item
