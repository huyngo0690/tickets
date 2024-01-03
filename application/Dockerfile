FROM python:3.11.6-alpine3.18 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    PYTHONPATH="/app" \
    VENV_PATH="/opt/pysetup/.venv" \
    PYSETUP_PATH="/opt/pysetup" \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

# Install python packages
RUN python -m pip install --upgrade pip
RUN apk update
RUN apk add --no-cache --virtual build-deps
RUN apk add --no-cache gcc libc-dev musl-dev libffi-dev python3-dev mysql-client pkgconfig redis
RUN apk add --no-cache --virtual libmysqlclient mariadb-dev mariadb-connector-c-dev
RUN pip install gunicorn bcrypt mysql-connector-python mysqlclient poetry==$POETRY_VERSION


WORKDIR $PYSETUP
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

FROM builder-base as production

WORKDIR /app
USER root
COPY . /app

RUN chmod +x ./run.sh
# Run Alembic migrations
RUN alembic upgrade head

EXPOSE 8080
CMD ["sh", "start.sh"]