from fastapi import APIRouter, Depends, HTTPException

from src.auth.permissions import require_permission
from src.database.session import get_db
from src.models.data import PayloadDataEntries, ReturnSources, ReturnDataEntries
from src.services.data_service import DataService

router = APIRouter()
tags = ["Data"]

def get_data_service(session=Depends(get_db)) -> DataService:
    return DataService(session=session)

@router.post("/data",
             response_model=ReturnDataEntries,
             tags=tags,
             dependencies=[Depends(require_permission(write=True))])
def post_data(payload: PayloadDataEntries, data_service: DataService=Depends(get_data_service)):
    data = data_service.post_data(data=payload.entries)
    if not data:
        raise HTTPException(status_code=500, detail="Unable to add records")
    return {
        "detail": "Success",
        "ingested": data
    }

@router.get("/data/sources",
            response_model=ReturnSources,
            tags=tags,
            dependencies=[Depends(require_permission(read=True))])
def get_data_sources(data_service: DataService=Depends(get_data_service)):
    result = data_service.get_sources()
    if not result:
        raise HTTPException(status_code=404, detail="Ingest table empty")
    return {
        "detail": "Success",
        "sources": result
    }