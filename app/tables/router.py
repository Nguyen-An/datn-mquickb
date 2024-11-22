from fastapi import APIRouter,Request, Depends, Response, status, HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from .models import *
from ..database import get_db
from pydantic import BaseModel
from .service import TableService
from fastapi.responses import JSONResponse
from app.common.responses_msg import *

router_tables = APIRouter(
    prefix="/tables",
    tags=["tables"],
    responses={404: {"description": "Not found"}},
)

@router_tables.get("")
async def get_profile_user(request:Request, page:int=1, page_size:int=20, db: Session = Depends(get_db)):
    try:
        t = await TableService.get_tables_service(db,page,page_size)
        return t
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_tables.post("")
async def create_table(request:Request, tableCreate : TableCreate, db: Session = Depends(get_db)):
    try:
        # print("request: ", request.state.info_user)
        t = await TableService.create_table_service(db, tableCreate)
        return t
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    

# api đặt bàn cho customer
@router_tables.put("/customer/{table_id}")
async def create_table(request:Request, table_id: int, db: Session = Depends(get_db)):
    try:
        info_user = request.state.info_user
        t = await TableService.book_table_customer(db, table_id, info_user)
        return t
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_tables.put("/{item_id}")
async def update_table_item(request:Request,item_id: int, tableUpdate : TableUpdate, db: Session = Depends(get_db)):
    try:
        mi = await TableService.update_table_item(db,item_id, tableUpdate)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_tables.delete("/{table_id}")
async def create_table(request:Request, table_id: int, db: Session = Depends(get_db)):
    try:
        # info_user = request.state.info_user
        t = await TableService.delete_table_service(db, table_id)
        return t
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    