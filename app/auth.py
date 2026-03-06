import hashlib
import secrets

from app.database import ApiKeys, Users
from fastapi import HTTPException
from sqlalchemy.orm import Session

def verify_api_key(database: Session, api_key: str) -> dict:
    
    user_id = database.query(ApiKeys).filter(ApiKeys.hashed_api_key == api_key).first()
    if user_id == None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user_id

def verify_resource_access(database: Session,
                  user_id: int,
                  can_read: bool | None = None,
                  can_write: bool | None = None,
                  is_admin: bool | None = None) -> bool:
    
    if can_read != None and can_write == None and is_admin == None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.can_read == can_read, Users.is_active == True).first()

    elif can_read == None and can_write != None and is_admin == None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.can_write == can_write, Users.is_active == True).first()
        
    elif is_admin != None:
        query_result = database.query(Users).filter(Users.user_id == user_id, Users.is_admin == is_admin, Users.is_active == True).first()

    if query_result == None:
        raise HTTPException(403)
        
    return True

def generate_key(database: Session) -> tuple[str, str]:

    # NOTE: Maybe replace below with catching an IntegrityError?
    # NOTE: The below might make a lot of unnecessary database calls.

    key = secrets.token_urlsafe(32)
    hashed_key = hash_key(key=key)
    if database.query(ApiKeys).filter(ApiKeys.hashed_api_key == hashed_key).first():
        return generate_key(database=database)
    else:
        return key, hashed_key
    
def hash_key(key: str) -> str:
    
    # NOTE: Hashing is a one way operation

    # String key needs to be encoded to bytes-like data
    encoded_key = key.encode(encoding="utf-8")

    # Create the hashing object
    hash_object = hashlib.sha256()

    # Update the hash object with the byte-like encoded key
    hash_object.update(encoded_key)

    # Transform the hashed key to a hexadecimal value
    hex_object = hash_object.hexdigest()
    return hex_object