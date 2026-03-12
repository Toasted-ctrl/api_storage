from fastapi import APIRouter

from app.models2 import status

router = APIRouter()

@router.get("/status", response_model=status.ReturnStatus, tags=["Status"])
def get_health():
    return {"status": "OK"}