from pydantic import BaseModel

class Entry(BaseModel):
    base_url: str
    url_ext: str | None = None
    params: dict | None = None
    data: dict | None = None
    status_code: int | None = None

class PayloadDataEntries(BaseModel):
    entries: list[Entry]

class ReturnDataEntries(BaseModel):
    detail: str
    ingested: list[Entry]

class Source(BaseModel):
    base_url: str
    url_ext: str

class ReturnSources(BaseModel):
    detail: str
    sources: list[Source]