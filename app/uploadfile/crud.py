from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import ChatbotData
from datetime import datetime

def create_file_db(db: Session, file_info: ChatbotData):
    db.add(file_info)
    db.commit()
    db.refresh(file_info)
    return file_info

def get_files_db(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999
        total_pages = 1
    total = db.query(ChatbotData).count()
    total_pages = (total + page_size - 1) // page_size
    items = db.query(ChatbotData).offset(offset).limit(limit).all()
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def delete_file(db: Session, key: str):
    file_to_delete = db.query(ChatbotData).filter(ChatbotData.key == key).one()
    db.delete(file_to_delete)
    db.commit()
    return file_to_delete