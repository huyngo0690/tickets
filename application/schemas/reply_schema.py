from pydantic import BaseModel


class ReplyCreateSchema(BaseModel):
    content: str


class ReplySchema(BaseModel):
    replyId: int
    ticketId: int
    content: str
    createdBy: str
    createdDate: str
