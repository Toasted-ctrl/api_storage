import os
import json

from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

app = FastAPI()
api_key_header = APIKeyHeader(name="API_KEY")
test_key = os.getenv("test_key")

class SuccessfulReturn(BaseModel):
    message: str

def is_allowed_post(api_key: str, access_type: str):
    if api_key != test_key: #TODO: Build function to verify api key
        raise HTTPException(401)
    
@app.get("/")
def read_root():
    return {"message": "Hello World"}

class SingleEntry(BaseModel):
    database: str
    table: str
    url: str
    params: dict | None
    data: dict

@app.post("/post_entry", response_model=SuccessfulReturn)
def post_single_entry(entry: SingleEntry, api_key=Depends(api_key_header)):
    is_allowed_post(api_key=api_key, access_type='r')
    print(entry.data)
    return {"message": "success"}