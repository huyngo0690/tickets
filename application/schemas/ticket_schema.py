from typing import Optional, List

from pydantic import BaseModel

from schemas.reply_schema import ReplySchema


class TicketCreateSchema(BaseModel):
    title: str
    description: str


class TicketSchema(BaseModel):
    ticketId: int
    title: str
    description: str
    createdDate: str
    createdBy: str
    replies: Optional[List[ReplySchema]] = []
