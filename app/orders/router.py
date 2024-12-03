from fastapi import APIRouter,Request, Depends, Response, status, HTTPException,BackgroundTasks

from sqlalchemy.orm import Session
from .models import *
from ..database import get_db
from pydantic import BaseModel
from .service import OrderService
from fastapi.responses import JSONResponse
from app.common.responses_msg import *

router_order = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)
    
@router_order.get("")
async def get_order(request:Request, page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    try:      
        info_user = request.state.info_user
        loi = await OrderService.get_order_service(db,info_user, page, page_size)
        
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_order.post("/staff-call")
async def create_staff_call(request:Request, staffCallCreate: StaffCallCreate, db: Session = Depends(get_db)):
    try:      
        info_user = request.state.info_user
        loi = await OrderService.create_staff_call_service(db,info_user, staffCallCreate)
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
# @router_order.put("/staff-call/{staff_call_id}")
# async def create_staff_call(request:Request, staffCallCreate: StaffCallCreate, db: Session = Depends(get_db)):
#     try:      
#         info_user = request.state.info_user
#         loi = await OrderService.create_staff_call_service(db,info_user, staffCallCreate)
#         return loi
#     except Exception as e:
#         return JSONResponse(
#             status_code=e.status_code,
#             content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
#         )  
    
@router_order.get("/staff-call")
async def get_staff_call(request:Request,page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    try:      
        info_user = request.state.info_user
        loi = await OrderService.get_staff_call_service(db,info_user, page, page_size)
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_order.post("/customer")
async def create_order(request:Request, orderItemCreate: listOrderItemCreate, db: Session = Depends(get_db)):
    try:      
        info_user = request.state.info_user
        loi = await OrderService.create_order_service(db,info_user, orderItemCreate)
        
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_order.get("/customer")
async def get_order_by_customer(request:Request, page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    try:      
        info_user = request.state.info_user
        loi = await OrderService.get_order_by_customer_service(db,info_user, page, page_size)
        
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  

@router_order.get("/order-items")
async def get_order(request:Request, page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    try:
        info_user = request.state.info_user
        loi = await OrderService.get_order_item_staff_service(db,info_user, page, page_size)
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    

@router_order.put("/order-items/{item_id}")
async def update_order_item_staff_service(request:Request, item_id: int, orderStatusUpdate: OrderStatusUpdate , db: Session = Depends(get_db)):
    try:
        info_user = request.state.info_user
        oi = await OrderService.update_order_item_staff_service(db, item_id, orderStatusUpdate)
        return oi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  

@router_order.post("/order-items")
async def get_order(request:Request, orderItemStaffCreate: OrderItemStaffCreate, db: Session = Depends(get_db)):
    try:
        info_user = request.state.info_user
        loi = await OrderService.create_order_item_staff_service(db,info_user, orderItemStaffCreate)
        return loi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    
@router_order.put("/pay/{table_id}")
async def pay_order(request:Request,table_id: int, db: Session = Depends(get_db)):
    try:
        mi = await OrderService.pay_order_service(db, table_id)
        return mi
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_error_response(e.detail, STT_CODE.get(e.detail, "Unknown error code"))
        )  
    