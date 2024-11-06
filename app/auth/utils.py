from datetime import datetime, timedelta
from jose import JWTError, jwt
from .models import *
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, Security, Request, Header, status
from .crud import *
from ..database import get_db
from ..common.responses_msg import *
from ..common.responses import *

security = HTTPBearer()
SECRET_KEY = os.getenv('SECRET_KEY','')
ALGORITHM = os.getenv('ALGORITHM','')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',30)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def checktoken(token: str, db: Session):
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
        return {
            "result": True,
            "data": payload
        }
    except Exception as e:
        return {
            "result": False,
            "data": None
        }

async def decode_token(token):
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
        return payload
    except JWTError:
        return None

def gettoken(request:Request):     
    token = request.headers.get('Authorization')  
    if token is None:
        return None
    res = token.split('Bearer ')[1] if token.startswith('Bearer ') else token    
    return res
