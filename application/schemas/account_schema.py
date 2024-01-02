from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr, Field


class AccountCreateSchema(BaseModel):
    username: str
    email: EmailStr = Field(examples=['abc@mail.com'])
    password: str
    isAdmin: bool = False


class StaffAccountCreateSchema(BaseModel):
    username: str
    email: EmailStr = Field(examples=['abc@mail.com'])
    password: str
    isAdmin: bool = True


class AccountSchema(BaseModel):
    uuid: str
    username: str


class AccountLoginResponseSchema(BaseModel):
    accessToken: str
    refreshToken: str
    profile: AccountSchema


class AccountLoginSchema(BaseModel):
    usernameOrEmail: str
    password: str
