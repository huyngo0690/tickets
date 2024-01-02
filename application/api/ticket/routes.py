from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends, status

from core.auth_bearer import JWTBearer
from core.errors_handler import ErrorMessage
from dependencies.account_service import get_account_service
from schemas.reply_schema import ReplySchema, ReplyCreateSchema
from services.account_services import AccountService

router = APIRouter()


@router.post("/{ticket_id}/replies/", response_model=ReplySchema)
async def add_reply_to_ticket(ticket_id: int,
                              reply_data: ReplyCreateSchema,
                              account_id=Depends(JWTBearer()),
                              account_service: AccountService = Depends(get_account_service)):
    return await account_service.create_reply(ticket_id, reply_data, account_id)


@router.get("/{ticket_id}/replies/", response_model=List[ReplySchema])
async def get_replies(ticket_id: int,
                      account_id=Depends(JWTBearer()),
                      account_service: AccountService = Depends(get_account_service)):
    return await account_service.get_replies_for_ticket(ticket_id)


@router.put("/replies/{reply_id}", response_model=ReplySchema)
async def update_reply(reply_id: int,
                       reply_data: ReplyCreateSchema,
                       account_id=Depends(JWTBearer()),
                       account_service: AccountService = Depends(get_account_service)):
    updated_reply = await account_service.update_reply(reply_id, reply_data.content, account_id)
    if not updated_reply:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.Permission_Error.value)
    return updated_reply


@router.delete("/replies/{reply_id}")
async def delete_reply(reply_id: int,
                       account_id=Depends(JWTBearer()),
                       account_service: AccountService = Depends(get_account_service)):
    success = await account_service.delete_reply(reply_id, account_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessage.Permission_Error.value)
    return {"message": "Reply deleted"}

