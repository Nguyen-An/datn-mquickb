from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import MenuItem

def create_menu_item_db(db: Session, menuItem: MenuItem):
    db.add(menuItem)
    db.commit()
    db.refresh(menuItem)
    return menuItem
