from pydantic import BaseModel

class ReturnSimple(BaseModel):
    message: str

class InputSingle(BaseModel):
    table: str
    url: str
    params: dict | None = None
    data: dict

class ReturnSingle(BaseModel):
    message: str
    api_key: str
    url: str
    table: str
    data: dict