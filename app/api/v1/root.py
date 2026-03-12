from fastapi import APIRouter

from app.models2 import root
from app.core.config import config

router = APIRouter()

@router.get("/", response_model = root.ReturnRoot, tags=["Root"])
def get_root():
    
    return {"message": "Hello There",
            "application_name": config.app_name,
            "version": config.app_version,
            "contact": {
                "maintainer": config.app_maintainer
            }}