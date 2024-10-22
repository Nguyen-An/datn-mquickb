from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_user_by_mail(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user