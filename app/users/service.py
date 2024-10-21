import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from jose import jwt
from os import getenv
from .crud import *
class UserService:
    async def get_profile_service(db: Session):
        user = get_users(db)
        return user