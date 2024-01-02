import datetime

from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import mapped_column

from db.base_class import Base


class Token(Base):
    __tablename__ = "tokens"
    id = Column(BigInteger, primary_key=True, index=True)
    account_id = mapped_column(ForeignKey("accounts.id"))
    refresh_token = Column(String(450), nullable=False)
    revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime)
