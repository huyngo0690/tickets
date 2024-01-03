import datetime

from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, ForeignKey, BigInteger, DateTime, Integer
from sqlalchemy.orm import mapped_column

from db.base_class import Base


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = mapped_column(ForeignKey("accounts.id"))
    refresh_token = Column(String(450), nullable=False)
    revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime)
