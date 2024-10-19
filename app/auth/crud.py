from sqlalchemy.orm import Session
from .models import *

def create_token(db: Session, token: Token):
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_token_by_code(db: Session, token: str):    
    return db.query(Token).filter(Token.token == token).first()

def get_list_roles(user,db: Session):
    if user['role_id'] == 'system_admin':
        return db.query(Role).all()
    elif user['role_id'] == 'company_admin':
        return db.query(Role).filter(Role.name != 'system_admin').all()
    else:
        return db.query(Role).all()
