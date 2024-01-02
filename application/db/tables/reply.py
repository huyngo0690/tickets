import datetime
from db.tables.ticket import Ticket
from sqlalchemy import (
    Column,
    ForeignKey,
    BigInteger, Text, DateTime, Integer,
)
from sqlalchemy.orm import relationship, mapped_column
from db.base_class import Base


class Reply(Base):
    __tablename__ = "replies"

    id = Column(BigInteger, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ticket_id = mapped_column(ForeignKey("tickets.id"))
    created_by_id = mapped_column(ForeignKey("accounts.id"))

    ticket = relationship("Ticket", back_populates="replies")
    account = relationship("Account", back_populates="replies")
