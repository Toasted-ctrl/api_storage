from pydantic import BaseModel
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReturnRoot(BaseModel):
    message: str
    version: str
    contact: dict

class ReturnHealth(BaseModel):
    status: str

class ReturnSimple(BaseModel):
    message: str

class InputDataSingle(BaseModel):
    url_primary: str
    url_extension: str
    params: dict | None = None
    status_code: int
    data: dict

class ReturnDataSingle(BaseModel):
    message: str
    url_primary: str
    url_extension: str
    data: dict
    params: dict | None = None

class InputNewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_admin: bool
    can_write: bool
    can_read: bool
    expiry_date: datetime | None = datetime.now() + relativedelta(months=6)

class ReturnNewUser(BaseModel):
    message: str
    new_user: dict

class ReturnDataSources(BaseModel):
    message: str
    sources: dict