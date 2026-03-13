from fastapi import APIRouter

from src.models.root import ReturnRoot
from src.core.config import config

router = APIRouter()

@router.get("/", response_model=ReturnRoot, tags=["Root"])
def get_root():
    
    return {
        "message": "Hello There",
        "application_name": config.app_name,
        "version": config.app_version,
        "contact": {
            "maintainer": config.app_maintainer
        }}