import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from jose import jwt
from os import getenv

class UserService:
    async def get_profile_service(db: Session):
        data = {
                "id": "123123", 
            }
        return data