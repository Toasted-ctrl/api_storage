from fastapi import APIRouter

from models.status import ReturnStatus

router = APIRouter()

@router.get("/status", response_model=ReturnStatus, tags=["Status"])
def get_health():
    return {
        "message": "OK"
    }