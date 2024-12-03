from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User, UserUpdate
from datetime import datetime

def get_users_db(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999
        total_pages = 1
    total = db.query(User).count()
    total_pages = (total + page_size - 1) // page_size
    items = db.query(User).offset(offset).limit(limit).all()
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_user_by_mail(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(db: Session, id: int):
    item = db.query(User).filter(User.id == id).first()
    return item

def create_user_db(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_db(db: Session, item_id: int, userUpdate: UserUpdate):
    db_item = db.query(User).filter(User.id == item_id).first()
    for key, value in userUpdate.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Cập nhật thời gian sửa đổi
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_user_by_id_db(db: Session, item_id: int):
    db_item = db.query(User).filter(User.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
