from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.company.models import Company
from .models import *
from ..user_manager.crud import get_user_by_mail
from ..common.encryption import verify_password
from ..common.responses_msg import *
from ..common.responses import OK, return_exception
from .utils import *
from .crud import *
from app.log.service import LogService, Log

log = LogService()
class AuthService:
    async def login(userLogin: UserLogin, db: Session):
        try:
            # get user
            user = get_user_by_mail(db, userLogin.email)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ITEM_NOT_FOUND)
            # check password
            check = verify_password(userLogin.password, user.password)
            if check != True:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password_incorrect")
            
            if user.active == False:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="account_not_active")
            
            user_company = db.query(Company).filter(Company.id == user.company_id).first()
            if user.role_id != 'system_admin':
                if user_company is None:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="dont_belong_to_any_company")
                if user_company.active == False:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="company_not_active")
            
            #get token
            data = {
                "id": user.id, 
                "user_name": user.user_name, 
                "email": user.email, 
                "company_id": user.company_id, 
                "company_name": user.company_name, 
                "phone_number": user.phone_number, 
                "role_id": user.role_id,
                "is_password_changed": user.is_password_changed
            }

            _token = create_access_token(data=data)
            token = Token(token = _token)
            create_token(db, token)

            #log
            logdata = Log(user_id = user.id, action = "login", is_success = True,created_at = datetime.now())            
            await log.create_log(db, logdata)

            return _token
        except Exception as e:
            print(e)
            return_exception(e)

    async def get_list_roles(user,db: Session):
        try:
            roles = get_list_roles(user,db)
            return OK(roles)
        except Exception as e:
            return_exception(e)
