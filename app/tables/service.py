import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from os import getenv
from .crud import *
from ..orders.crud import *
from ..common.encryption import *
from sqlalchemy.orm import Session

class TableService:
    async def get_tables_service(db: Session, page:int, page_size:int):
        user = get_tables_db(db, page, page_size)
        return user
    
    async def create_table_service(db: Session, tableCreate : TableCreate):
        new_table = Table(
            table_name = tableCreate.table_name,
            qr_code =tableCreate.qr_code,
            status =tableCreate.status,
        )

        table = create_table_db(db, new_table)
        return table

    async def update_table_item(db: Session,item_id: int, tableUpdate : TableUpdate):
        existing_item = get_table_by_id(db, item_id)
        if not existing_item:
            raise HTTPException(
                status_code=404, detail=f"Table with id {item_id} not found."
        )

        menuItem = update_table_db(db, item_id, tableUpdate)
        return menuItem


    async def book_table_customer(db: Session, table_id: int, info_user):
        # Kiểm tra xem bàn còn trống không
        table = get_table_by_id(db, table_id)

        if table is None:
            raise HTTPException(status_code=404, detail="TABLE_NOT_FOUND")
        if table.status != "available":
            raise HTTPException(status_code=400, detail="TABLE_HAS_BEEN_USED")
        
        # Kiểm tra xem user này đã đặt bàn nào chưa
        orders = check_user_order_table(db, info_user.get("id"))
        if orders: 
            raise HTTPException(status_code=400, detail="USER_HAS_BOOKED_TABLE")
        
        # Tạo order -> pending
        new_order = Order(
            user_id = info_user.get("id"),
            table_id = table_id,
            total_amount = 0,
            status = 'pending',
        )
        order = create_order_db(db, new_order)

        # Cập nhật trạng thái table -> booked 
        tableUpdate = TableUpdate(
            table_name = table.table_name,
            qr_code = table.qr_code,
            status = "booked" 
        )

        update_table_db(db,table.id, tableUpdate)
        data = {
            "table_id": table.id,
            "order_id": order.id
        }
        
        return data
    
    async def delete_table_service(db: Session,item_id: int):
        try:
            existing_item = get_table_by_id(db, item_id)
            if not existing_item:
                raise HTTPException(
                    status_code=404, detail=f"MenuItem with id {item_id} not found."
            )

            table = delete_table_service(db, item_id)
            return table
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")