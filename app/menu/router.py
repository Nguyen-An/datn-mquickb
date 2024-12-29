from fastapi import APIRouter,Request, Depends, Response, status, HTTPException,BackgroundTasks

from sqlalchemy.orm import Session
from .models import *
from ..database import get_db
from pydantic import BaseModel
from .service import MenuService
from fastapi.responses import JSONResponse
from app.common.responses_msg import *

router_menus = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={404: {"description": "Not found"}},
)

@router_menus.get("")
async def get_list_menu_item(request:Request, page:int=1, page_size:int=20, key_word:str="", db: Session = Depends(get_db)):
    try:
        mi = await MenuService.get_list_menu_item(db,page,page_size, key_word)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_menus.get("/customer")
async def get_list_menu_item(request:Request, page:int=1, page_size:int=20, db: Session = Depends(get_db)):
    try:
        info_user = request.state.info_user
        mi = await MenuService.get_menu_for_customer_service(db,info_user,page,page_size)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_menus.post("")
async def create_menu_item(request:Request, menuItemCreate : MenuItemCreate, db: Session = Depends(get_db)):
    try:
        # print("request: ", request.state.info_user)
        mi = await MenuService.create_menu_item(db, menuItemCreate)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  

@router_menus.put("/{item_id}")
async def update_menu_item(request:Request,item_id: int, menuItemUpdate : MenuItemUpdate, db: Session = Depends(get_db)):
    try:
        mi = await MenuService.update_menu_item(db,item_id, menuItemUpdate)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_menus.delete("/{item_id}")
async def delete_menu_item(request:Request,item_id: int, db: Session = Depends(get_db)):
    try:
        mi = await MenuService.delete_menu_item(db,item_id)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  