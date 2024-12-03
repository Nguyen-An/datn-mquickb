from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import MenuItem
from datetime import datetime

def create_menu_item_db(db: Session, menuItem: MenuItem):
    db.add(menuItem)
    db.commit()
    db.refresh(menuItem)
    return menuItem

def get_list_menu_item(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999
        total_pages = 1
    total = db.query(MenuItem).count()
    total_pages = (total + page_size - 1) // page_size
    items = db.query(MenuItem).offset(offset).limit(limit).all()
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_menu_for_customer_db(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999
        total_pages = 1
    total = db.query(MenuItem).filter(MenuItem.is_available == True).count()
    total_pages = (total + page_size - 1) // page_size
    items = db.query(MenuItem).filter(MenuItem.is_available == True).offset(offset).limit(limit).all()
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_menu_item_by_id(db: Session, item_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    return item

def update_menu_item_db(db: Session, item_id: int, menuItem: MenuItem):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    for key, value in menuItem.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Cập nhật thời gian sửa đổi
    db_item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_menu_item_db(db: Session, item_id: int):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
