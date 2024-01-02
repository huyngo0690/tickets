from typing import Any

import uuid
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())
