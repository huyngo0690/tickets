from pydantic import BaseModel


class ReplyCreateSchema(BaseModel):
    content: str


class ReplySchema(BaseModel):
    id: int
    ticket_id: int
    content: str
    createdBy: str
    createdDate: str
