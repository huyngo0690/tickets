# Import all the tables, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from db.tables.account import Account  # noqa
from db.tables.ticket import Ticket  # noqa
from db.tables.token import Token  # noqa
from db.tables.reply import Reply  # noqa
