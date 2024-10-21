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

@router_users.get("/profile")
async def get_profile_user(request:Request, db: Session = Depends(get_db)):
    try:
        u = await UserService.get_profile_service(db)
        
        return u
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, ERR_CODE.get(e.detail, "Unknown error code"))
        )  