from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import ChatbotData
from datetime import datetime

def create_file_db(db: Session, file_info: ChatbotData):
    db.add(file_info)
    db.commit()
    db.refresh(file_info)
    return file_info
