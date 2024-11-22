from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User

def get_users_db(db: Session, page: int, page_size: int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
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

def create_user_db(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
