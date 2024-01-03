from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi import Depends, status

from core.auth_bearer import JWTBearer
from core.errors_handler import ErrorMessage
from dependencies.account_service import get_account_service
from schemas import ticket_schema
from schemas.reply_schema import ReplySchema, ReplyCreateSchema
from schemas.ticket_schema import TicketCreateSchema, TicketSchema
from services.account_services import AccountService

router = APIRouter()


@router.post("/{ticket_id}/replies/", response_model=ReplySchema)
async def add_reply_to_ticket(
    ticket_id: int,
    reply_data: ReplyCreateSchema,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.create_reply(ticket_id, reply_data, account_id)


@router.get("/{ticket_id}/replies/", response_model=List[ReplySchema])
async def get_replies(
    ticket_id: int,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.get_replies_for_ticket(ticket_id)


@router.put("/replies/{reply_id}", response_model=ReplySchema)
async def update_reply(
    reply_id: int,
    reply_data: ReplyCreateSchema,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    updated_reply = await account_service.update_reply(
        reply_id, reply_data.content, account_id
    )
    if not updated_reply:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessage.Permission_Error.value,
        )
    return updated_reply


@router.delete("/replies/{reply_id}")
async def delete_reply(
    reply_id: int,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    success = await account_service.delete_reply(reply_id, account_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessage.Permission_Error.value,
        )
    return {"message": "Reply deleted"}


@router.post(
    "/ticket/",
    status_code=status.HTTP_201_CREATED,
    response_model=ticket_schema.TicketSchema,
)
async def create_ticket(
    ticket_data: TicketCreateSchema,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    if await account_service.is_staff(account_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can create tickets",
        )
    return await account_service.create_ticket(account_id, ticket_data)


@router.get("/tickets/")
async def get_tickets(
    page: Optional[int] = 0,
    pageSize: Optional[int] = 10,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.get_tickets(account_id, page, pageSize)


@router.get("/ticket/{ticket_id}", response_model=TicketSchema)
async def get_ticket_details(
    ticket_id: int,
    account_id=Depends(JWTBearer()),
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.get_ticket_details(ticket_id, account_id)
