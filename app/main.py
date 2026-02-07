from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_NAME = "API-Key"

app = FastAPI()
api_key_header_read = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key_access_read(api_key: str = Depends(api_key_header_read)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

@app.get("/")
def read_root():
    return 200, {"message": "Hello World"}

@app.post("/post_entry", dependencies=verify_api_key_access_read)
def post_single_entry():
    return 200, {"message": "Success"}