from fastapi import APIRouter, Depends, Request
from ..database import get_db
from ..common.responses import common_responses
from sqlalchemy.orm import Session
from .models import *
from .service import AuthService
from app.auth.utils import decode_token, gettoken, verify_token
router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router_auth.post("", responses=common_responses)
async def login(userLogin: UserLogin, db: Session = Depends(get_db)):
    return await AuthService.login(userLogin, db)

# @router_auth.post("/test", responses=common_responses)
# def register(test: Test,request: Request, db: Session = Depends(get_db)):
#     return {
#         "test": test,
#         "request": request.state.info_user,
#     }

@router_auth.get("/roles", responses=common_responses)
async def get_list_roles(request:Request,db: Session = Depends(get_db)):
    token = gettoken(request) 
    user = await decode_token(token)
    return await AuthService.get_list_roles(user,db)
