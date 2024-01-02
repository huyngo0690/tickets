import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
    Boolean, BigInteger, DateTime,
)
from sqlalchemy.orm import relationship
from db.tables.reply import Reply
from db.tables.ticket import Ticket
from db.base_class import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean(), default=False)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    tickets = relationship("Ticket", back_populates="account")
    replies = relationship("Reply", back_populates="account")
