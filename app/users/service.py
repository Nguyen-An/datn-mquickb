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

class UserService:
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
            role = "customer_qr",
            phone_number = userCreate.phone_number,
        )

        user = create_user_db(db, new_user)
        return user