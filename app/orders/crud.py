from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.sql import text

def create_order_item_db(db: Session, orderItem: OrderItem):
    db.add(orderItem)
    db.commit()
    db.refresh(orderItem)
    return orderItem

def create_order_db(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def create_staff_call_db(db: Session, staffCall: StaffCall):
    db.add(staffCall)
    db.commit()
    db.refresh(staffCall)
    return staffCall

def get_order_db(db: Session,order_id, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
        limit = 9999999999
    if order_id is None:
        items = db.query(OrderItem).offset(offset).limit(limit).all()
        total = db.query(OrderItem).count()
    else:
        items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        total = db.query(OrderItem).filter(OrderItem.order_id == order_id).count()

    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_staff_call_db(db: Session, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
        limit = 9999999999
    items = db.query(StaffCall).offset(offset).limit(limit).all()
    total = db.query(StaffCall).count()

    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_order_items_db(db: Session, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 1
        limit = 9999999999
    items = db.query(OrderItem).offset(offset).limit(limit).all()
    total = db.query(OrderItem).count()
    total_pages = (total + page_size - 1) // page_size

    query_get_list = text("""
        SELECT oi.*, 
            mi.name AS menu_item_name
        FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        ORDER BY oi.id
        LIMIT :limit OFFSET :offset;
    """)

    # Thực thi câu lệnh SQL với phân trang
    result_list = db.execute(query_get_list, {"limit": 10, "offset": 0})

    # Lấy kết quả dưới dạng danh sách các từ điển
    result = result_list.mappings().all()

    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": result
    }


def get_order_id_by_user_id(db: Session, user_id: int):
    item = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).first()
    return item

def get_order_in_progress_by_table_id(db: Session, table_id: int):
    item = db.query(Order).filter(Order.table_id == table_id, Order.status == "in_progress").order_by(desc(Order.created_at)).first()
    return item

def check_user_order_table(db: Session, user_id: int):
    item = db.query(Order).filter(Order.user_id == user_id, Order.status.in_(["pending", "in_progress"])).order_by(desc(Order.created_at)).all()
    return item

def update_order_db(db: Session, item_id: int, orderUpdate: OrderUpdate):
    db_item = db.query(Order).filter(Order.id == item_id).first()
    for key, value in orderUpdate.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Cập nhật thời gian sửa đổi
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item