from app import auth
from app import models
from app.database import get_database
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

app = FastAPI(version="0.0.1", contact={"maintainer": "Toasted-ctrl"})
api_key_header = APIKeyHeader(name="api-key")
    
@app.get("/", response_model = models.ReturnRoot)
def root():
    
    return {"message": "Hello There",
            "version": app.version,
            "contact": app.contact}

@app.get("/health", response_model=models.ReturnHealth)
def health():
    
    return {"status": "OK"}

@app.post("/single", response_model = models.ReturnDataSingle)
def single(payload: models.InputDataSingle,
           db: Session = Depends(get_database),
           api_key: str = Depends(api_key_header)):
    
    user_id = auth.verify_api_key(database=db, api_key=api_key)
    auth.verify_resource_access(database=db, user_id=user_id.id, can_write=True)

    # TODO: Finalize implementation
    
    return {"message": "Success",
            "url": payload.url,
            "table": payload.table,
            "data": payload.data}

@app.post("/add_user", response_model = models.ReturnNewUser)
def add_user(payload: models.InputNewUser,
             db: Session = Depends(get_database),
             api_key: str = Depends(api_key_header)):
    
    user_id = auth.verify_api_key(database=db, api_key=api_key)
    auth.verify_resource_access(database=db, user_id=user_id.id, is_admin=True)

    # TODO: Finalize implementation
    
    return {"message": "Success",
            "api_key": api_key,
            "new_user_api_key": "TEST-KEY-NEW-USER-123",
            "expiry_date": payload.expiry_date}