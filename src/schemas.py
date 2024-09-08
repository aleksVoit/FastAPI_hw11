from datetime import date  # new_user = User(name='Alice', birthdate=date(1995, 5, 17))
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
import re


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
