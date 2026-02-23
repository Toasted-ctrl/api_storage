from app.database import ApiKeys, Users
from fastapi import HTTPException
from sqlalchemy.orm import Session

def verify_api_key(database: Session, api_key: str) -> dict:
    
    user_id = database.query(ApiKeys).filter(ApiKeys.api_key == api_key).first()
    if user_id == None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user_id

def verify_resource_access(database: Session,
                  user_id: int,
                  can_read: bool | None = None,
                  can_write: bool | None = None,
                  is_admin: bool | None = None) -> bool:
    
    if can_read != None and can_write == None and is_admin == None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.can_read == can_read).first()

    elif can_read == None and can_write != None and is_admin == None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.can_write == can_write).first()
        
    elif is_admin != None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.is_admin == is_admin).first()

    if query_result == None:
        raise HTTPException(403)
        
    return True