import logging
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from core.date_utils import DateUtils
from core.errors_handler import ErrorMessage
from db.tables.account import Account
from db.tables.reply import Reply
from db.tables.ticket import Ticket
from schemas.reply_schema import ReplySchema
from schemas.ticket_schema import TicketSchema


class TicketRepository:
    def __init__(self, session):
        self.session = session

    async def create_ticket(self, account_id, ticket_data):
        try:
            new_ticket = Ticket(**ticket_data.dict(), created_by_id=account_id)
            (account_name,) = (
                self.session.query(Account.user_name)
                .filter(Account.id == account_id)
                .first()
            )
            self.session.add(new_ticket)
            self.session.commit()
            self.session.refresh(new_ticket)
            return TicketSchema(
                ticketId=new_ticket.id,
                title=new_ticket.title,
                description=new_ticket.description,
                createdDate=DateUtils.full_datetime_to_str(new_ticket.created_date),
                createdBy=account_name,
            )
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
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def get_ticket_details(self, ticket_id: int, account_id: int):
        try:
            ticket = (
                self.session.query(
                    Ticket.title,
                    Ticket.description,
                    Ticket.created_by_id,
                    Account.user_name,
                )
                .filter(
                    Ticket.id == ticket_id,
                    Account.id == Ticket.created_by_id,
                )
                .first()
            )

            if ticket.created_by_id != account_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=ErrorMessage.Permission_Error.value,
                )

            replies = (
                self.session.query(
                    Reply.id,
                    Reply.content,
                    Reply.created_by_id,
                    Reply.created_at,
                    Account.user_name,
                )
                .filter(Reply.ticket_id == ticket_id, Account.id == Reply.created_by_id)
                .order_by(Reply.created_at.desc())
                .all()
            )
            return TicketSchema(
                ticketId=ticket_id,
                title=ticket.title,
                description=ticket.title,
                createdDate=DateUtils.full_datetime_to_str(ticket.title),
                createdBy=ticket.user_name,
                replies=[
                    ReplySchema(
                        replyId=reply.id,
                        ticketId=ticket_id,
                        content=reply.content,
                        createdBy=reply.user_name,
                        createdDate=DateUtils.full_datetime_to_str(reply.created_at),
                    )
                    for reply in replies
                ],
            )
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def get_tickets(
        self, is_staff: bool, account_id: int, page: int, page_size: int
    ):
        try:
            offset = page * page_size
            limit = page_size
            query = self.session.query(
                Ticket.id,
                Ticket.title,
                Ticket.description,
                Ticket.created_date,
                Account.user_name,
            ).filter(Account.id == Ticket.created_by_id)
            if not is_staff:
                query = query.filter(Ticket.created_by_id == account_id)

            total = query.count()
            response = {"total": total, "data": []}
            tickets = (
                query.order_by(Ticket.created_date.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            for ticket in tickets:
                response["data"].append(
                    TicketSchema(
                        ticketId=ticket.id,
                        title=ticket.title,
                        description=ticket.description,
                        createdBy=ticket.user_name,
                        createdDate=DateUtils.full_datetime_to_str(ticket.created_date),
                    )
                )
            return response
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def create_reply(self, ticket_id, reply_data, account_id):
        try:
            new_reply = Reply(
                **reply_data.dict(), ticket_id=ticket_id, created_by_id=account_id
            )
            (account_name,) = (
                self.session.query(Account.user_name)
                .filter(Account.id == account_id)
                .first()
            )
            self.session.add(new_reply)
            self.session.commit()
            self.session.refresh(new_reply)
            new_reply = ReplySchema(
                replyId=new_reply.id,
                ticketId=new_reply.ticket_id,
                content=new_reply.content,
                createdBy=account_name,
                createdDate=DateUtils.full_datetime_to_str(new_reply.created_at),
            )
            return new_reply
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
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

    async def get_replies_for_ticket(self, ticket_id: int):
        try:
            replies = (
                self.session.query(
                    Reply.id,
                    Reply.ticket_id,
                    Reply.content,
                    Reply.created_at,
                    Account.user_name,
                )
                .filter(Reply.ticket_id == ticket_id, Account.id == Reply.created_by_id)
                .all()
            )
            return [
                ReplySchema(
                    replyId=reply.id,
                    ticketId=reply.ticket_id,
                    content=reply.content,
                    createdBy=reply.user_name,
                    createdDate=DateUtils.full_datetime_to_str(reply.created_at),
                )
                for reply in replies
            ]
        except Exception as e:
            logging.info(f"{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def update_reply(self, reply_id: int, new_content: str, account_id: int):
        try:
            reply = self.session.query(Reply).filter(Reply.id == reply_id).first()
            if reply.created_by_id != account_id:
                return None
            (account_name,) = (
                self.session.query(Account.user_name)
                .filter(Account.id == account_id)
                .first()
            )
            reply.content = new_content
            self.session.add(reply)
            self.session.commit()
            self.session.refresh(reply)
            return ReplySchema(
                replyId=reply.id,
                ticketId=reply.ticket_id,
                content=reply.content,
                createdBy=account_name,
                createdDate=DateUtils.full_datetime_to_str(reply.created_at),
            )
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
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

    async def delete_reply(self, reply_id: int, account_id: int):
        try:
            reply = self.session.query(Reply).filter(Reply.id == reply_id).first()
            if reply and reply.created_by_id == account_id:
                self.session.delete(reply)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as err:
            self.session.rollback()
            err = str(err.__dict__["orig"])
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
