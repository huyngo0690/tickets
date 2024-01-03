from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi import Depends, status

from core.auth_bearer import JWTBearer
from dependencies.account_service import get_account_service
from schemas import account_schema, ticket_schema
from schemas.ticket_schema import TicketCreateSchema
from services.account_services import AccountService

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=account_schema.ShowAccountSchema,
)
async def register_user(
    request: account_schema.AccountCreateSchema,
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.register_account(request)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: account_schema.AccountLoginSchema,
    account_service: AccountService = Depends(get_account_service),
):
    user = await account_service.authenticate_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
        )
    access_token = await account_service.create_access_token(user.id)
    _refresh_token = await account_service.create_refresh_token(user.id)
    return {"accessToken": access_token, "refreshToken": _refresh_token}


@router.post("/refresh_token/")
async def refresh_token(
    _refresh_token: str, account_service: AccountService = Depends(get_account_service)
):
    new_access_token, new_refresh_token = await account_service.refresh_token(
        _refresh_token
    )
    return {"accessToken": new_access_token, "refreshToken": new_refresh_token}


@router.post("/logout/")
async def logout(
    _refresh_token: str, account_service: AccountService = Depends(get_account_service)
):
    await account_service.revoke_refresh_token(_refresh_token)
    return {"message": "Logged out successfully"}
