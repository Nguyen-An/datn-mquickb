import json
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy import JSON
from .crud import *
from ..common.responses_msg import *
from .models import *
from datetime import datetime
from os import getenv
from .crud import *
from ..common.encryption import *
from sqlalchemy.orm import Session
from ..tables.crud import *

class OrderService:
    async def create_order_service(db: Session,info_user, orderItemCreate: listOrderItemCreate):
        # Kiểm tra xem có order_id chưa
        if info_user.get("order_ID") == None:
            raise HTTPException(status_code=400, detail="ORDER_ID_REQUIRED")
        if info_user.get("table_id") == None:
            raise HTTPException(status_code=400, detail="TABLE_ID_REQUIRED")

        existing_table_item = get_table_by_id(db, info_user.get("table_id"))
        if not existing_table_item:
            raise HTTPException(
                status_code=404, detail=f"Table with not found."
        )
        if existing_table_item.status != "in_use":
            raise HTTPException(
                status_code=404, detail="TABLE_NOT_USE"
        )

        # Kiểm tra xem các menu_item_id có tôn tại hoặc hoạt động không
        list_order_item = []

        # Thêm order_item vào order 
        for orderItem in orderItemCreate.items:
            new_order_item = OrderItem(
                order_id = info_user.get("order_ID"),
                menu_item_id = orderItem.menu_item_id,
                quantity = orderItem.quantity,
                status = 'pending',
                price = orderItem.price,
                created_by = info_user.get("id"),
                updated_by = info_user.get("id")
            )

            order_item = create_order_item_db(db, new_order_item)
            list_order_item.append(order_item)
        return list_order_item
    
    async def create_order_item_staff_service(db: Session,info_user, orderItemStaffCreate: OrderItemStaffCreate):
        # Kiểm tra xem có order_id chưa
        existing_table_item = get_table_by_id(db, orderItemStaffCreate.table_id)
        if not existing_table_item:
            raise HTTPException(
                status_code=404, detail=f"Table with not found."
        )

        if existing_table_item.status != "in_use":
            raise HTTPException(
                status_code=404, detail="TABLE_NOT_USE"
        )

        existing_order = get_order_in_progress_by_table_id(db, orderItemStaffCreate.table_id)

        if not existing_order:
            raise HTTPException(
                status_code=404, detail="ORDER_DOES_NOT_EXIST"
        )

        # Thêm order_item vào order 
        new_order_item = OrderItem(
            order_id = existing_order.id,
            menu_item_id = orderItemStaffCreate.menu_item_id,
            quantity = orderItemStaffCreate.quantity,
            status = orderItemStaffCreate.status,
            created_by = info_user.get("id"),
            updated_by = info_user.get("id")
        )

        order_item = create_order_item_db(db, new_order_item)
        return order_item

    async def get_order_service(db: Session, info_user, page: int, page_size: int):
        list_order = get_order_db(db, page, page_size)
        return list_order
    
    async def get_order_by_customer_service(db: Session, info_user, page: int, page_size: int):
        order_id = info_user.get('order_ID')

        list_order = get_order_items_db(db, order_id, page, page_size)
        return list_order
    
    async def get_staff_call_service(db: Session, info_user, page: int, page_size: int):
        list_staff_call = get_staff_call_db(db, page, page_size)
        return list_staff_call
    
    async def create_staff_call_service(db: Session,info_user, staffCallCreate: StaffCallCreate):
        new_staff_call = StaffCall(
            table_id = staffCallCreate.table_id,
            reason = staffCallCreate.reason,
            created_by = info_user.get("id"),
            updated_by = info_user.get("id"),
            status = 'pending'
        )

        staff_call = create_staff_call_db(db, new_staff_call)
        return staff_call
    
    async def pay_order_service(db: Session, table_id):
        # Lấy order_id theo table
        table = get_table_by_id(db, table_id)

        if table is None:
            raise HTTPException(status_code=404, detail="TABLE_NOT_FOUND")
        if table.status != "in_use":
            raise HTTPException(status_code=400, detail="TABLE_NOT_IN_USED")
        if table.order_id is None:
            raise HTTPException(status_code=400, detail="THERE_ARE_NO_ORDERS_FOR_THIS_TABLE")
        
        # Kiểm tra Tất cả order_item phải có trạng thái đã phục vụ hoặc từ chối
        # q_order_items = get_all_order_items_by_order_id(db, table.order_id)

        # Cập nhật trạng thái order_item thành đã thanh toán
        ids = update_order_items_status(db, table.order_id, "paid", "rejected")

        # Cập nhật trạng thái bàn
        tableUpdate = TableUpdate(
            table_name = table.table_name,
            qr_code = table.qr_code,
            status = "available",
            order_id = None
        )
        update_table_db(db,table.id, tableUpdate)

        # Cập nhật order thành đã thanh toán
        
        return ids