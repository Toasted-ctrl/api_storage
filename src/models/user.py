from pydantic import BaseModel
from typing import Any

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
    detail: str
    user: UserDetailed

class ReturnUsers(BaseModel):
    detail: str
    users: list[UserSimple]

class PayloadUpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_admin: bool | None = None
    can_read: bool | None = None
    can_write: bool | None = None
    is_active: bool | None = None