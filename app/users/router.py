from fastapi import APIRouter,Request, Depends, Response, status, HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from .models import *
from ..database import get_db
from pydantic import BaseModel
from .service import UserService
from fastapi.responses import JSONResponse
from app.common.responses_msg import *

router_users = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router_users.get("")
async def get_users(request:Request, page:int=1, page_size:int=20, key_word:str="", db: Session = Depends(get_db)):
    try:
        u = await UserService.get_users_service(db,page,page_size,key_word)
        return u
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_users.post("")
async def create_user(request:Request, userCreate: UserCreate, db: Session = Depends(get_db)):
    try:        
        u = await UserService.create_user_service(db, userCreate)
        
        return u
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_users.put("/{item_id}")
async def update_user(request:Request,item_id: int, userUpdate : UserUpdate, db: Session = Depends(get_db)):
    try:
        mi = await UserService.update_user_service(db,item_id, userUpdate)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_users.delete("/{item_id}")
async def delete_user(request:Request,item_id: int, db: Session = Depends(get_db)):
    try:
        mi = await UserService.delete_user_service(db,item_id)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_users.get("/profile")
async def get_profile_user(request:Request, db: Session = Depends(get_db)):
    try:
        # print("request: ", request.state.info_user)
        u = await UserService.get_profile_service(db)
        
        return u
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    