import logging
import os
import time
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from api.user import routes as account_routes
from api.staff import routes as staff_routes
from api.ticket import routes as ticket_routes
from core.settings import settings
from db.base_class import Base
from dependencies.session import engine

app = FastAPI(title="User Management", version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def include_app(_app):
    _app.include_router(account_routes.router, tags=["user"], prefix="/api/user")
    _app.include_router(staff_routes.router, tags=["staff"], prefix="/api/staff")
    _app.include_router(ticket_routes.router, tags=["ticket"], prefix="/api")


def create_tables():  # new
    Base.metadata.create_all(engine)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.time()
    try:
        logging.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response
    except Exception as err:
        logging.info(f"Request: {request.url} failed - Details: {err} ")
        return JSONResponse(status_code=400, content={"message": err})
    finally:
        process_time = time.time() - start_time
        logging.info(f"Request: {request.url} finished in {process_time}")


if not os.path.exists("logs"):
    os.makedirs("logs")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("logs/app.log", maxBytes=100000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    errors = [{"field": e["loc"][1], "error": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Data integrity error."},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error."},
    )


if __name__ == "__main__":
    include_app(app)
    create_tables()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
