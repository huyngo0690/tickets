from typing import Optional

from pydantic import BaseModel


class ReplyCreateSchema(BaseModel):
    content: str


class ReplySchema(BaseModel):
    replyId: int
    ticketId: Optional[int] = None
    content: str
    createdBy: str
    createdDate: str
