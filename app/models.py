from pydantic import BaseModel

class PostSingleEntry(BaseModel):
    database: str
    table: str
    url: str
    params: dict | None = None
    data: dict

class ReturnSuccessSimple(BaseModel):
    message: str