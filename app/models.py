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
    data: dict

class ReturnDataSingle(BaseModel):
    message: str
    url_primary: str
    url_extension: str
    data: dict
    params: dict | None = None

class InputNewUser(BaseModel):
    first_name: str
    last_name: str
    is_admin: bool
    can_write: bool
    can_read: bool
    expiry_date: datetime | None = datetime.now() + relativedelta(months=6)

class ReturnNewUser(BaseModel):
    message: str
    api_key: str
    new_user_api_key: str
    expiry_date: datetime