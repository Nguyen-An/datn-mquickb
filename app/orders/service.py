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

class OrderService:
    async def create_order_service(db: Session,info_user, orderItemCreate: listOrderItemCreate):
        # Kiểm tra xem có order_id chưa
        if orderItemCreate.order_id == None:
            raise HTTPException(status_code=400, detail="ORDER_ID_REQUIRED")

        # Kiểm tra xem các menu_item_id có tôn tại hoặc hoạt động không

        list_order_item = []
        # Thêm order_item vào order 
        for orderItem in orderItemCreate.items:
            new_order_item = OrderItem(
                order_id = orderItemCreate.order_id,
                menu_item_id = orderItem.menu_item_id,
                quantity = orderItem.quantity,
                status = 'pending',
                created_by = info_user.get("id"),
                updated_by = info_user.get("id")
            )

            order_item = create_order_item_db(db, new_order_item)
            list_order_item.append(order_item)

        return list_order_item

    async def get_order_service(db: Session, info_user, page: int, page_size: int):
        order_id = None
        
        # if info_user.get("role_id") != "manager" and info_user.get("role_id") != "staff":
        #     order = get_order_id_by_user_id(db, int(info_user.get("user_id")))
        #     order_id = order.id

        list_order = get_order_db(db, order_id, page, page_size)
        return list_order