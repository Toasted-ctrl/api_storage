from app import models
from app import database
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

app = FastAPI(version="0.0.1", contact={"maintainer": "Toasted-ctrl"})
api_key_header = APIKeyHeader(name="api-key")
db_con = database.get_database()
    
@app.get("/", response_model = models.ReturnRoot)
def root():
    
    return {"message": "Hello There",
            "version": app.version,
            "contact": app.contact}

@app.post("/single", response_model = models.ReturnDataSingle)
def single(payload: models.InputDataSingle,
           db: Session = Depends(db_con),
           api_key: str = Depends(api_key_header)):

    # TODO: Build auth function
    # TODO: Finalize implementation
    # TODO: Rewrite all tests
    
    return {"message": "Success",
            "api_key": api_key,
            "url": payload.url,
            "table": payload.table,
            "data": payload.data}

@app.post("/add_user", response_model = models.ReturnNewUser)
def add_user(payload: models.InputNewUser,
             db: Session = Depends(db_con),
             api_key: str = Depends(api_key_header)):

    # TODO: Build auth function
    # TODO: Finalize implementation
    # TODO: Rewrite all tests
    
    return {"message": "Success",
            "api_key": "test-key",
            "new_user_api_key": api_key,
            "expiry_date": payload.expiry_date}