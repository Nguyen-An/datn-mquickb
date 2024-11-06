from fastapi import APIRouter, Depends, Request
from ..database import get_db
from sqlalchemy.orm import Session
from .models import *
from .service import AuthService
from fastapi.responses import JSONResponse
from ..common.responses_msg import *
from ..common.responses import *

# from app.auth.utils import decode_token, gettoken, verify_token
router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# api đăng nhập cho 'customer', 'staff', 'manager'
@router_auth.post("", responses=common_responses)
async def login(userLogin: UserLogin, db: Session = Depends(get_db)):
    try:
        return await AuthService.login(userLogin, db)
        
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )   

# api đăng nhập cho 'customer', 'customer_qr' để đặt bàn
@router_auth.post("/qr", responses=common_responses)
async def login(userLoginQR: UserLoginQR, db: Session = Depends(get_db)):
    try:
        return await AuthService.loginQR(userLoginQR, db)
        
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )   