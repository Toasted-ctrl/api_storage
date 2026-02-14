import os

from app import models
from app import auth
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

load_dotenv()

app = FastAPI()
api_key_header = APIKeyHeader(name="API_KEY")

db_database_ingest = os.getenv("db_database_ingest")
    
@app.get("/", response_model=models.ReturnSimple)
def read_root():
    return {"message": "Hello World"}

@app.post("/post_single", response_model=models.ReturnPostSingle)
def post_single(entry: models.InputSingleEntry, api_key: str = Depends(api_key_header)):
    user_id = auth.verify_api_key(api_key=api_key, database=db_database_ingest, access_type='Write-only')
    return {"message": "Data added successfully", "user_id": user_id, "data": entry.data}

# TODO: Build new function where auth is handled as dependency of main function call.