from pydantic import BaseModel

class Contact(BaseModel):
    maintainer: str

class ReturnRoot(BaseModel):
    message: str
    version: str
    contact: Contact

class ReturnHealth(BaseModel):
    status: str

class ReturnSimple(BaseModel):
    message: str

class IngestData(BaseModel):
    url_primary: str
    url_extension: str
    params: dict | None = None
    status_code: int
    data: dict | None = None

class InputAddData(BaseModel):
    entries: list[IngestData]

class ReturnAddData(BaseModel):
    message: str
    entries: list[IngestData]

class InputNewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_admin: bool
    can_write: bool
    can_read: bool

class Source(BaseModel):
    url_primary: str
    url_extension: str

class ReturnDataSources(BaseModel):
    message: str
    sources: list[Source]

class UserDetailed(BaseModel):
    user_id: int
    email: str
    can_read: bool
    can_write: bool
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool

class UserSimple(BaseModel):
    user_id: int
    email: str

class ReturnUser(BaseModel):
    message: str
    user: UserDetailed

class ReturnUpdatedUser(BaseModel):
    message: str
    updates: int
    user: UserDetailed

class InputUpdateUser(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    can_read: bool | None = None
    can_write: bool | None = None
    can_read: bool | None = None
    is_active: bool | None = None
    is_admin: bool | None = None

class NewUser(BaseModel):
    user: UserDetailed
    api_key: str

class ReturnNewUser(BaseModel):
    message: str
    new_user: NewUser

class ReturnUsers(BaseModel):
    message: str
    users: list[UserSimple]