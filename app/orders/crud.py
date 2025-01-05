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

def get_order_db(db: Session, page: int, page_size: int, status: str = None):
    # Tính toán offset và limit
    offset = (page - 1) * page_size
    limit = page_size

    # Nếu page == -1, bỏ qua giới hạn phân trang
    if page == -1:
        offset = 0
        limit = None  # Không giới hạn số lượng

    # Xây dựng query
    query = db.query(OrderItem)
    
    # Thêm điều kiện lọc theo status nếu được truyền vào
    if status:
        query = query.filter(OrderItem.status == status)

    # Tính tổng số lượng bản ghi
    total = query.count()

    # Tính tổng số trang
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1

    # Lấy danh sách đơn hàng với phân trang
    items = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "data": items,
    }

def get_staff_call_db(db: Session, order_id: int, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999
    items = db.query(StaffCall).filter(StaffCall.order_id == order_id).order_by(desc(StaffCall.id)).offset(offset).limit(limit).all()
    total = db.query(StaffCall).count()

    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": items
        }

def get_order_items_db(db: Session, order_id, page:int, page_size:int):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 999999
    items = db.query(OrderItem).offset(offset).limit(limit).all()
    total = db.query(OrderItem).count()
    total_pages = (total + page_size - 1) // page_size

    query_get_list = text("""
        SELECT oi.*, 
            mi.name AS menu_item_name
        FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = :order_id
        ORDER BY oi.id
        LIMIT :limit OFFSET :offset;
    """)
    # Thực thi câu lệnh SQL với phân trang
    result_list = db.execute(query_get_list, {"order_id": order_id, "limit": limit, "offset": offset})

    # Lấy kết quả dưới dạng danh sách các từ điển
    result = result_list.mappings().all()

    return {
        "total": total, 
        "total_pages": total_pages, 
        "current_page": page, 
        "page_size": page_size, 
        "data": result
    }

def get_order_item_staff_db(db: Session, page: int, page_size: int, status: str = None):
    offset = (int(page) - 1) * int(page_size)
    limit = page_size
    if page == -1:
        offset = 0
        limit = 9999999999

    # Xử lý điều kiện WHERE cho status
    status_condition = ""
    params = {"limit": limit, "offset": offset}
    if status and status.lower() != "all":
        status_condition = "WHERE oi.status = :status"
        params["status"] = status

    # Truy vấn tổng số lượng bản ghi
    count_query = text(f"""
        SELECT COUNT(*) 
        FROM order_items oi
        {status_condition}
    """)
    total = db.execute(count_query, params).scalar()

    # Tính tổng số trang
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1

    # Truy vấn danh sách order items
    query_get_list = text(f"""
        SELECT oi.*, 
            mi.name AS menu_item_name,
            t.table_name AS name_table
        FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        LEFT JOIN tables t ON t.order_id = oi.order_id
        {status_condition}
        ORDER BY oi.id DESC
        LIMIT :limit OFFSET :offset;
    """)

    # Thực thi truy vấn danh sách
    result_list = db.execute(query_get_list, params)

    # Lấy kết quả
    result = result_list.mappings().all()

    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "data": result
    }

def get_all_order_items_by_order_id(db: Session, order_id):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return items

def update_order_items_status(db: Session, order_id: int, new_status: str = "paid", excluded_status: str = "rejected"):
    updated_items = db.query(OrderItem).filter(
            OrderItem.order_id == order_id,
            OrderItem.status != excluded_status
        ).all()
    # Nếu không có bản ghi nào để cập nhật
    if not updated_items:
        return []

    # Cập nhật trạng thái của tất cả các bản ghi đã tìm được
    for item in updated_items:
        item.status = new_status
        db.add(item)

    # Lưu thay đổi vào cơ sở dữ liệu
        db.commit()

    # Trả về số lượng bản ghi đã cập nhật và danh sách ID của các bản ghi đó
    updated_ids = [item.id for item in updated_items]
    return updated_ids

def get_order_id_by_user_id(db: Session, user_id: int):
    item = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).first()
    return item

def get_order_item_by_id(db: Session, order_item_id: int):
    item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    return item

def update_status_order_item_db(db: Session, item_id: int, orderStatusUpdate: OrderStatusUpdate):
    db_item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    for key, value in orderStatusUpdate.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Cập nhật thời gian sửa đổi
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item

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


def get_dashboard_revenue_db(db: Session):
    query_get_list = text("""
        SELECT
            EXTRACT(MONTH FROM oi.created_at) AS month,
            SUM(oi.quantity * oi.price) AS total_revenue
        FROM
            order_items oi
        WHERE
            EXTRACT(YEAR FROM oi.created_at) = 2024
            AND oi.status = 'paid'
        GROUP BY
            EXTRACT(MONTH FROM oi.created_at)
        ORDER BY
            month;
    """)

    result_list = db.execute(query_get_list)

    result = result_list.mappings().all()

    return result


def get_dashboard_order_db(db: Session):
    query_get_list = text("""
        SELECT
            EXTRACT(MONTH FROM o.created_at) AS month,
            COUNT(o.id) AS total_orders
        FROM
            orders o
        WHERE
            EXTRACT(YEAR FROM o.created_at) = 2024
        GROUP BY
            EXTRACT(MONTH FROM o.created_at)
        ORDER BY
            month;
    """)

    result_list = db.execute(query_get_list)

    result = result_list.mappings().all()

    return result

def get_bill_by_order_db(db: Session, order_id: int):
    query_get_list = text("""
        SELECT SUM(oi.price * oi.quantity) as total
        FROM order_items oi
        WHERE oi.order_id = :order_id
        AND oi.status NOT IN ('rejected')
    """)

    result = db.execute(query_get_list, {"order_id": order_id}).scalar()
    return result