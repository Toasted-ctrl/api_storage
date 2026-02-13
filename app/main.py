from app import models
from app import auth
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

load_dotenv()

app = FastAPI()
api_key_header = APIKeyHeader(name="API_KEY")
    
@app.get("/", response_model=models.ReturnSuccessSimple)
def read_root():
    return {"message": "Hello World"}

@app.post("/post_single", response_model=models.ReturnSuccessSimple)
def post_single(entry: models.PostSingleEntry, api_key=Depends(api_key_header)):
    user_id = auth.verify_api_key(api_key=api_key)
    return {"message": "success"}