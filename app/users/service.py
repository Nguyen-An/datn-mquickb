import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from os import getenv
from .crud import *
from ..common.encryption import *
from sqlalchemy.orm import Session

class UserService:
    async def get_users_service(db: Session, page:int, page_size:int):
        user = get_users_db(db, page, page_size)
        return user
    
    async def get_profile_service(db: Session):
        user = get_users(db)
        return user
    
    async def create_user_service(db: Session, userCreate: UserCreate):
        # check role
        password_hash = hash_password("123456aA@")

        new_user = User(
            name = userCreate.name,
            email = userCreate.email,
            password_hash = password_hash,
            role = userCreate.role,
            phone_number = userCreate.phone_number,
        )

        user = create_user_db(db, new_user)
        return user
    
    async def update_user_service(db: Session,item_id: int, userUpdate: UserUpdate):
        existing_item = get_table_by_id(db, item_id)
        if not existing_item:
            raise HTTPException(
                status_code=404, detail=f"User with id {item_id} not found."
        )

        menuItem = update_user_db(db, item_id, userUpdate)
        return menuItem
    
    