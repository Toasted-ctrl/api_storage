from app import models
from app import auth
from fastapi import FastAPI, Depends

app = FastAPI()

# Create auth dependencies
dependency_auth = auth.verify_api_key()
dependency_auth_admin = auth.verify_api_key(is_admin=True)
    
@app.get("/", response_model=models.ReturnSimple)
def root():
    
    return {"message": "Hello World"}

@app.post("/single", response_model=models.ReturnDataSingle)
def single(payload: models.InputDataSingle, user=Depends(dependency=dependency_auth)):

    # TODO: Finalize implementation
    
    return {"message": "Success",
            "api_key": user['api_key'],
            "url": payload.url,
            "table": payload.table,
            "data": payload.data}

@app.post("/add_user", response_model=models.ReturnNewUser)
def add_user(payload: models.InputNewUser, user=Depends(dependency=dependency_auth_admin)):

    # TODO: Finalize implementation
    
    return {"message": "Success",
            "api_key": user['api_key'],
            "new_user_api_key": "test-new-user-api-key-123",
            "expiry_date": payload.expiry_date}