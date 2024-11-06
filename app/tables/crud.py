from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime

def get_tables_db(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
        limit = 9999999999
        total_pages = 1
    total = db.query(Table).count()
    total_pages = (total + page_size - 1) // page_size
    items = db.query(Table).offset(offset).limit(limit).all()
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def create_table_db(db: Session, table: Table):
    db.add(table)
    db.commit()
    db.refresh(table)
    return table

def get_table_by_id(db: Session, id: int):
    item = db.query(Table).filter(Table.id == id).first()
    return item

def get_table_by_qr(db: Session, qr_code: str):
    item = db.query(Table).filter(Table.qr_code == qr_code).first()
    return item

def update_table_db(db: Session, item_id: int, tableUpdate: TableUpdate):
    db_item = db.query(Table).filter(Table.id == item_id).first()
    for key, value in tableUpdate.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Cập nhật thời gian sửa đổi
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item