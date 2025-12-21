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


from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ContactCreate(BaseModel):
    name: str
    email: EmailStr

class ContactResponse(ContactCreate):
    id: int



from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
