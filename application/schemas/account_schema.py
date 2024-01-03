from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr, Field


class AccountCreateSchema(BaseModel):
    username: str
    email: EmailStr = Field(examples=['abc@mail.com'])
    password: str
    isAdmin: bool = False


class ShowAccountSchema(BaseModel):
    username: str
    email: EmailStr
    isAdmin: bool

    class Config:
        from_attributes = True


class StaffAccountCreateSchema(BaseModel):
    username: str
    email: EmailStr = Field(examples=['abc@mail.com'])
    password: str
    isAdmin: bool = True


class AccountLoginResponseSchema(BaseModel):
    accessToken: str
    refreshToken: str


class AccountLoginSchema(BaseModel):
    usernameOrEmail: str
    password: str
