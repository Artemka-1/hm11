from datetime import date
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=120)
    last_name: str = Field(..., max_length=120)
    email: EmailStr
    phone: str = Field(..., max_length=50)
    birthday: date
    additional: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=120)
    last_name: Optional[str] = Field(None, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    birthday: Optional[date] = None
    additional: Optional[str] = None

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
