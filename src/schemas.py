
from typing import Optional

from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactSchema(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=20)
    birthday: date
    additional_info: Optional[str] = Field(None, max_length=200)
    completed: Optional[bool] = False
#
# class TodoSchema(BaseModel):
#     title: str = Field(max_length=50, min_length=3)
#     description: str = Field(max_length=200, min_length=5)
#     completed: Optional[bool] = False
#
#
class ContactUpdateSchema(ContactSchema):
    completed: bool
#
#
class ContactResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponseSchema | None

    class Config:
        from_attributes = True


