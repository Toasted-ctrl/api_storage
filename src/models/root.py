from pydantic import BaseModel

class Contact(BaseModel):
    maintainer: str

class ReturnRoot(BaseModel):
    message: str
    version: str
    application_name: str
    contact: Contact