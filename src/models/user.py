from pydantic import BaseModel

class UserSimple(BaseModel):
    email: str
    user_id: int

class UserDetailed(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    can_read: bool
    can_write: bool
    user_id: int
    is_active: bool

class PayloadNewUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    can_read: bool
    can_write: bool

class NewUser(BaseModel):
    user: UserDetailed
    api_key: str

class ReturnNewUser(BaseModel):
    detail: str
    new_user: NewUser

class ReturnUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    can_read: bool
    can_write: bool
    user_id: bool
    is_active: bool
    is_admin: bool

class ReturnUsers(BaseModel):
    detail: str
    users: list[UserSimple]