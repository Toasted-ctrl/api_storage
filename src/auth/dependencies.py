from cachetools import TTLCache
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from src.auth.hashing import hash_sha256
from src.database.schema import ApiKeys, Users
from src.database.session import get_db

api_key_header = APIKeyHeader(name="X-api-key", auto_error=False)

# Use cache to store the user for 60 seconds
cache = TTLCache(maxsize=10_000, ttl=60)

async def get_user(db: Session=Depends(get_db),
                   api_key: str=Depends(api_key_header)) -> Users:
    
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing API key")
    
    hashed_key = hash_sha256(input=api_key)
    if hashed_key in cache:
        return cache[hashed_key]

    id = (
        db.query(ApiKeys.user_id)
        .filter(
            ApiKeys.hashed_api_key == hashed_key,
            ApiKeys.is_valid == True)
        .first()
    )

    if not id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid API key")
    
    user = db.query(Users).filter(Users.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User inactive")
    
    cache[hashed_key] = user
    
    return user