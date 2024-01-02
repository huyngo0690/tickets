from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies.session import get_db
from repositories.account_repository import AccountRepository
from repositories.ticket_repository import TicketRepository
from services.account_services import AccountService


def get_account_service(db: Session = Depends(get_db)) -> AccountService:
    account_repository = AccountRepository(db)
    ticket_repository = TicketRepository(db)
    return AccountService(account_repository, ticket_repository)
