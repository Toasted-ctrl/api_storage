from pydantic import BaseModel

class UserDetailed(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    can_read: bool
    can_write: bool

class UserSimple(BaseModel):
    email: str
    user_id: int

class PayloadNewUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    can_read: bool
    can_write: bool

class NewUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    can_read: bool
    can_write: bool
    id: int
    api_key: str

class ReturnNewUser(BaseModel):
    detail: str
    new_user: NewUser

class ReturnUsers(BaseModel):
    detail: str
    users: list[UserSimple]