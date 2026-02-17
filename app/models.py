from pydantic import BaseModel
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReturnRoot(BaseModel):
    message: str
    version: str
    contact: str

class ReturnSimple(BaseModel):
    message: str

class InputDataSingle(BaseModel):
    table: str
    url: str
    params: dict | None = None
    data: dict

class ReturnDataSingle(BaseModel):
    message: str
    api_key: str
    url: str
    table: str
    data: dict

class InputNewUser(BaseModel):
    user_first_name: str
    user_last_name: str
    access_type: str
    expiry_date: datetime | None = datetime.now() + relativedelta(months=6)

class ReturnNewUser(BaseModel):
    message: str
    api_key: str
    new_user_api_key: str
    expiry_date: datetime