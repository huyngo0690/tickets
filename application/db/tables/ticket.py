import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    BigInteger, Text, DateTime,
)
from sqlalchemy.orm import mapped_column, relationship
from db.base_class import Base


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    created_by_id = mapped_column(ForeignKey("accounts.id"), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="tickets")
    replies = relationship("Reply", back_populates="ticket")
