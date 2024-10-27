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
    async def get_list_menu_item(db: Session):
        try:
            return 1
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
