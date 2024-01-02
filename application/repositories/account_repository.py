import datetime
import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from core.auth import get_hashed_password
from core.errors_handler import ErrorMessage, ApiStatusMessage
from db.tables.account import Account
from db.tables.token import Token
from schemas.account_schema import AccountCreateSchema


class AccountRepository:
    def __init__(self, session):
        self.session = session

    async def create_account(self, request: AccountCreateSchema):
        try:
            user_name = request.username
            account = (
                self.session.query(Account)
                .filter(Account.user_name == user_name)
                .first()
            )
            if account:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.ACCOUNT_EXISTED.value,
                )
            encrypted_password = get_hashed_password(request.password)
            new_account = Account(
                user_name=user_name,
                email=request.email,
                password=encrypted_password,
                is_admin=request.isAdmin,
            )
            self.session.add(new_account)
            self.session.commit()
            return {"message": ApiStatusMessage.SUCCESS.value}
        except SQLAlchemyError as err:
            err = str(err.__dict__["orig"])
            self.session.rollback()
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )
        except Exception as e:
            self.session.rollback()
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def update_account(self, account_id: str, request):
        pass

    async def delete_account(self, account_id: str):
        try:
            return {"message": ApiStatusMessage.SUCCESS.value}
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )

    async def get_account(self, account_id) -> Account:
        return self.session.query(Account).filter(Account.id == account_id).first()

    async def get_user_by_username_or_email(self, username_or_email):
        try:
            account = self.session.query(Account).filter(
                (Account.user_name == username_or_email) |
                (Account.email == username_or_email)
            ).first()
            account.last_login = datetime.datetime.utcnow()
            self.session.add(account)
            self.session.commit()
            return account
        except SQLAlchemyError as err:
            err = str(err.__dict__["orig"])
            self.session.rollback()
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )
        except Exception as e:
            logging.info(f"{str(e)}")
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def create_refresh_token(self, account_id: int, token: str, expires_at: datetime):
        try:
            new_refresh_token = Token(account_id=account_id, refresh_token=token, expires_at=expires_at)
            self.session.add(new_refresh_token)
            self.session.commit()
            return new_refresh_token
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )
        except Exception as e:
            self.session.rollback()
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def get_refresh_token(self, token: str):
        try:
            return self.session.query(Token).filter(Token.token == token).first()
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def revoke_refresh_token(self, token: str):
        try:
            db_token = self.get_refresh_token(token)
            if db_token:
                db_token.revoked = True
                self.session.commit()
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )
        except Exception as e:
            self.session.rollback()
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
