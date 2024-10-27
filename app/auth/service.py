from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import *
from ..users.crud import *
from ..common.encryption import verify_password
from ..common.responses_msg import *
from ..common.responses import OK, return_exception
from .utils import *
from .crud import *
class AuthService:
    async def login(userLogin: UserLogin, db: Session):
        try:
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
                "phone_number": user.phone_number, 
                "role_id": user.role,
            }

            _token = create_access_token(data=data)
            return _token
        except Exception as e:
            raise HTTPException(status_code=500, detail="INTERNAL_SERVER_ERROR")
