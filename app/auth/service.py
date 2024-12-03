from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import *
from ..users.crud import *
from ..common.encryption import verify_password
from ..common.responses_msg import *
from ..common.responses import OK, return_exception
from .utils import *
from .crud import *
from ..orders.crud import *
from ..tables.crud import *

class AuthService:
    async def login(userLogin: UserLogin, db: Session):
        # get user
        user = get_user_by_mail(db, userLogin.email)
        if user is None:
            raise HTTPException(status_code=404, detail="ITEM_NOT_FOUND")
        
        # check password
        check = verify_password(userLogin.password, user.password_hash)
        if check != True:
            raise HTTPException(status_code=401, detail="PASSWORD_INCORRECT")
        
        #get token
        data = { 
            "id": user.id, 
            "name": user.name, 
            "email": user.email, 
            "phone_number": user.phone_number , 
            "role_id": user.role,
        }

        _token = create_access_token(data=data)
        return _token

    async def loginQR(userLoginQR: UserLoginQR, db: Session):
        if userLoginQR.type == 'customer':
            # check user
            user = get_user_by_mail(db, userLoginQR.email)
            if user is None:
                raise HTTPException(status_code=404, detail="ITEM_NOT_FOUND")
            if user.role != 'customer':
                raise HTTPException(status_code=400, detail="INCORRECT_LOGIN_TYPE")
            check = verify_password(userLoginQR.password, user.password_hash)
            if check != True:
                raise HTTPException(status_code=401, detail="PASSWORD_INCORRECT")
            
            # Kiểm tra xem user này đã đặt bàn chưa, chưa đặt thì thông báo chưa đặt bàn, không cho đăng nhập
            orders = check_user_order_table(db, user.id)
            if not orders: 
                raise HTTPException(status_code=400, detail="USER_HAS_NOT_BOOKED_TABLE")
            
            # Nếu tìm thấy nhiều hơn 1 đơn đang chờ thì thông báo gọi nhân viên
            if len(orders) > 1: 
                raise HTTPException(status_code=400, detail="USER_HAS_MORE_THAN_ORDER_OR_PENDING_ORDER")
            
            # Cập nhật trạng thái bàn: booked -> in_use 
            order = orders[0]
            table = get_table_by_id(db, order.table_id)

            if table is None:
                raise HTTPException(status_code=404, detail="TABLE_NOT_FOUND")
            if table.status != "booked":
                raise HTTPException(status_code=400, detail="TABLE_NOT_USED")
            
            tableUpdate = TableUpdate(
                table_name = table.table_name,
                qr_code = table.qr_code,
                status = "in_use" 
            )
            update_table_db(db,table.id, tableUpdate)

            # Cập nhật trạng thái order: pending -> in_progress
            orderUpdate = OrderUpdate(
                table_id = order.table_id,
                total_amount = order.total_amount,
                status = "in_progress" 
            )
            update_order_db(db,order.id, orderUpdate)

            # get token
            data = { 
                "id": user.id, 
                "name": user.name, 
                "email": user.email, 
                "phone_number": user.phone_number , 
                "role_id": user.role,
                "order_ID": order.id,
                "table_id": table.id,
            }

            _token = create_access_token(data=data)
            return _token
        elif userLoginQR.type == 'customer_qr':
            table = get_table_by_qr(db, userLoginQR.qrcode)

            if table is None:
                raise HTTPException(status_code=404, detail="TABLE_NOT_FOUND")
            if table.status != "available":
                raise HTTPException(status_code=400, detail="TABLE_HAS_BEEN_USED")
            
            # Tạo user mới
            new_user = User(
                name = userLoginQR.name,
                email = "",
                password_hash = "",
                role = "customer_qr",
                phone_number = ""
            )

            new_user_qr = create_user_db(db, new_user)

            # Tạo order có trạng thái -> in_progress
            new_order = Order(
                user_id = new_user_qr.id,
                table_id = table.id,
                total_amount = 0,
                status = 'in_progress',
            )
            order = create_order_db(db, new_order)

            # Cập nhật status bàn -> in_use 
            tableUpdate = TableUpdate(
                table_name = table.table_name,
                qr_code = table.qr_code,
                status = "in_use", 
                order_id = order.id
            )
            update_table_db(db,table.id, tableUpdate)

            # get token
            data = { 
                "id": new_user_qr.id, 
                "name": new_user_qr.name, 
                "email": new_user_qr.email, 
                "phone_number": new_user_qr.phone_number , 
                "role_id": new_user_qr.role,
                "order_ID": order.id,
                "table_id": table.id,
            }

            _token = create_access_token(data=data)
            return _token
        else:
            raise HTTPException(status_code=400, detail="INCORRECT_LOGIN_TYPE")
