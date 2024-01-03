from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from dependencies.session import get_db
from api.user import routes as account_routes
from api.staff import routes as staff_routes
from api.ticket import routes as ticket_routes
from main import app
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app.include_router(account_routes.router, tags=["user"], prefix="/api/user")
app.include_router(staff_routes.router, tags=["staff"], prefix="/api/staff")
app.include_router(ticket_routes.router, tags=["ticket"], prefix="/api/ticket")

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user():
    response = client.post(
        "/api/user/register",
        json={
            "username": "testuser",
            "email": "testuser@abc.com",
            "password": "testing",
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_login():
    response = client.post(
        "/api/user/login/", json={"usernameOrEmail": "testuser", "password": "testing"}
    )
    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_create_ticket():
    login_response = client.post(
        "/api/user/login/", json={"usernameOrEmail": "testuser", "password": "testing"}
    )
    token = login_response.json()["accessToken"]
    response = client.post(
        "/api/user/createTicket",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Ticket", "description": "This is a test"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Ticket"


def test_get_tickets():
    login_response = client.post(
        "/api/user/login/", data={"username": "testuser", "password": "testing"}
    )
    token = login_response.json()["accessToken"]
    response = client.get("/tickets/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_reply():
    login_response = client.post(
        "/api/user/login/", data={"username": "testuser", "password": "testing"}
    )
    token = login_response.json()["accessToken"]
    response = client.post(
        "/1/replies/",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": "Test Reply"},
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Test Reply"
