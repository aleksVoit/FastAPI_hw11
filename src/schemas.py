from datetime import date, datetime  # new_user = User(name='Alice', birthdate=date(1995, 5, 17))
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(pattern=r'^\+?[1-9]\d{1,14}$')
    birthday: date


class NotesContact(BaseModel):
    notes: Optional[List[str]]


class ContactResponse(ContactModel):
    id: int
    notes: Optional[List[str]]

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = 'User successfully created'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

