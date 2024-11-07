from fastapi import APIRouter,Request, Depends, Response

from .service import UploadFileService
from fastapi import UploadFile
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from .models import *

router_uploadfile = APIRouter(
    prefix="/uploadfile",
    tags=["uploadfile"],
    responses={404: {"description": "Not found"}},
)

upload = UploadFileService()
@router_uploadfile.post("/upload/avatar")
async def upload_avatar(request:Request,file: UploadFile, db: Session = Depends(get_db)):  
    user_info = request.state.info_user
    try:
        key =  await upload.upload_avatar_to_s3(user_info,file,db)        
        return key
    except Exception as e:        
        return Response(status_code=e.status_code, content=str(e)) 