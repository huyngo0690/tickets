import datetime

import jwt
from fastapi import HTTPException, status

from core.auth import verify_password
from core.settings import settings
from repositories.account_repository import AccountRepository
from repositories.ticket_repository import TicketRepository
from schemas.account_schema import AccountCreateSchema, AccountLoginSchema


class AccountService:
    def __init__(self, account_repository: AccountRepository, ticket_repository: TicketRepository):
        self.account_repository = account_repository
        self.ticket_repository = ticket_repository

    async def register_account(self, account_data):
        return await self.account_repository.create_account(account_data)

    async def create_refresh_token(self, user_id: int):
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        token_payload = {"exp": expire, "sub": str(user_id)}
        refresh_token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        await self.account_repository.create_refresh_token(user_id, refresh_token, expire)
        return refresh_token

    @staticmethod
    async def create_access_token(user_id: int):
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {"exp": expires_delta, "sub": str(user_id)}
        access_token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)

        return access_token

    async def refresh_token(self, token: str):
        db_token = await self.account_repository.get_refresh_token(token)
        if not db_token or db_token.revoked or db_token.expires_at < datetime.datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return self.create_access_token(db_token.user_id), await self.create_refresh_token(db_token.user_id)

    async def authenticate_user(self, account_schema: AccountLoginSchema):
        account = await self.account_repository.get_user_by_username_or_email(account_schema.usernameOrEmail)
        if account and verify_password(account_schema.password, account.password):
            return account
        return None

    async def revoke_refresh_token(self, token: str):
        await self.account_repository.revoke_refresh_token(token)

    async def create_ticket(self, account_id: int, ticket_data):
        return await self.ticket_repository.create_ticket(account_id, ticket_data)

    async def get_ticket(self, ticket_id: int):
        return await self.ticket_repository.get_ticket(ticket_id)

    async def get_tickets_by_account_id(self, page: int, page_size: int, account_id: int):
        return await self.ticket_repository.get_tickets_by_account(page, page_size, account_id)

    async def get_tickets(self, page: int, page_size: int, user_id: int = None):
        return await self.ticket_repository.get_tickets(page, page_size, user_id)

    async def create_reply(self, ticket_id: int, reply_data, user_id: int):
        return await self.ticket_repository.create_reply(ticket_id, reply_data, user_id)

    async def is_staff(self, account_id: int) -> bool:
        user = await self.account_repository.get_account(account_id)
        return user.is_admin
