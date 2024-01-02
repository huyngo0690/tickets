import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from core.date_utils import DateUtils
from db.tables.account import Account
from db.tables.reply import Reply
from db.tables.ticket import Ticket
from schemas.ticket_schema import TicketSchema


class TicketRepository:
    def __init__(self, session):
        self.session = session

    async def create_ticket(self, account_id, ticket_data):
        try:
            new_ticket = Ticket(**ticket_data.dict(), created_by_id=account_id)
            self.session.add(new_ticket)
            self.session.commit()
            self.session.refresh(new_ticket)
            return new_ticket
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )

    async def get_ticket(self, ticket_id):
        try:
            return self.session.query(Ticket).filter(Ticket.id == ticket_id).first()
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )

    async def get_tickets_by_account(self, account_id: int, page: int = None, page_size: int = None):
        try:
            query = self.session.query(Ticket).filter(Ticket.created_by_id == account_id).order_by(
                Ticket.created_date.desc())
            total = query.count()
            if page or page_size:
                offset = page * page_size
                limit = page_size
                query = query.offset(offset).limit(limit)

            tickets = query.all()
            response = {"total": total, "data": []}
            for ticket in tickets:
                response["data"].append({
                    "ticket_id": ticket.id,
                    "title": ticket.title,
                    "description": ticket.description,
                    "createDate": DateUtils.full_datetime_to_str(ticket.created_date)
                })
            return response
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def get_tickets(self, page: int, page_size: int, account_id: int = None):
        try:
            offset = page * page_size
            limit = page_size
            query = self.session.query(Ticket.id, Ticket.title, Ticket.description, Ticket.created_date, Account.user_name).filter(
                Ticket.created_by_id == Account.id)
            if account_id:
                query = query.filter(Ticket.created_by_id == account_id)
            total = query.count()
            response = {"total": total, "data": []}
            tickets = query.order_by(Ticket.created_date.desc()).offset(offset).limit(limit).all()
            for ticket in tickets:
                response["data"].append(TicketSchema(
                    ticketId=ticket.id,
                    title=ticket.title,
                    description=ticket.description,
                    createdBy=ticket.user_name,
                    createdDate=DateUtils.full_datetime_to_str(ticket.created_date)
                ))
            return response
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def create_reply(self, ticket_id, reply_data, account_id):
        try:
            new_reply = Reply(**reply_data.dict(), ticket_id=ticket_id, created_by_id=account_id)
            self.session.add(new_reply)
            self.session.commit()
            self.session.refresh(new_reply)
            return new_reply
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
            logging.error(f"{err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )
