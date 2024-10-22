from fastapi import APIRouter, Depends, Request
from ..database import get_db
from sqlalchemy.orm import Session
from .models import *
from .service import AuthService
# from app.auth.utils import decode_token, gettoken, verify_token
router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router_auth.post("")
async def login(userLogin: UserLogin, db: Session = Depends(get_db)):
    return await AuthService.login(userLogin, db)
