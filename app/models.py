from pydantic import BaseModel

class InputSingleEntry(BaseModel):
    table: str
    url: str
    params: dict | None = None
    data: dict

class ReturnSimple(BaseModel):
    message: str

class ReturnPostSingle(BaseModel):
    message: str
    user_id: str
    data: dict