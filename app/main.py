from app import models
from app import auth
from fastapi import FastAPI, Depends

app = FastAPI()
dependecy_auth = auth.verify_api_key()
    
@app.get("/", response_model=models.ReturnSimple)
def root():
    
    return {"message": "Hello World"}

@app.post("/single", response_model=models.ReturnSingle)
def single_2(payload: models.InputSingle, user=Depends(dependency=dependecy_auth)):
    
    return {"message": "Success",
            "api_key": user['api_key'],
            "url": payload.url,
            "table": payload.table,
            "data": payload.data}