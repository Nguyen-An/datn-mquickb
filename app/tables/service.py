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
