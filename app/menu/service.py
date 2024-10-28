import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from os import getenv
from .crud import *
from ..common.encryption import *

class MenuService: 
    async def get_list_menu_item(db: Session, page:int, page_size:int):
        try:
            list_menu_items = get_list_menu_item(db, page, page_size)
            return list_menu_items
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")


    async def create_menu_item(db: Session, menuItemCreate : MenuItemCreate):
        try:
            new_menuItem = MenuItem(
                name = menuItemCreate.name,
                description = menuItemCreate.description,
                image_link = menuItemCreate.image_link,
                price = menuItemCreate.price,
                category = menuItemCreate.category,
                is_available = menuItemCreate.is_available
            )

            menuItem = create_menu_item_db(db, new_menuItem)
            return menuItem
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")
        
    async def update_menu_item(db: Session,item_id: int, menuItemCreate : MenuItemCreate):
        try:
            existing_item = get_menu_item_by_id(db, item_id)
            if not existing_item:
                raise HTTPException(
                    status_code=404, detail=f"MenuItem with id {item_id} not found."
            )

            menuItem = update_menu_item_db(db, item_id, menuItemCreate)
            return menuItem
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")

    async def delete_menu_item(db: Session,item_id: int):
        try:
            existing_item = get_menu_item_by_id(db, item_id)
            if not existing_item:
                raise HTTPException(
                    status_code=404, detail=f"MenuItem with id {item_id} not found."
            )

            menuItem = delete_menu_item_db(db, item_id)
            return menuItem
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")