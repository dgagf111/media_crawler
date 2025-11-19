import asyncio
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import pythonprojecttemplate.api.api_router as api_module
import pythonprojecttemplate.api.auth.auth_service as auth_service
from pythonprojecttemplate.api.auth.auth_service import get_current_user, get_db
from pythonprojecttemplate.api.auth.token_service import create_tokens, revoke_tokens
from pythonprojecttemplate.api.exception.custom_exceptions import (
    InvalidTokenException,
    TokenRevokedException,
)


@pytest.fixture()
def client(monkeypatch):
    app = FastAPI()
    app.include_router(api_module.api_router)

    async def override_get_db():
        yield None

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    yield test_client
    app.dependency_overrides.clear()


def test_token_endpoint_returns_tokens(client, monkeypatch):
    async def fake_auth(session, username, password):
        assert username == "alice"
        assert password == "secret"
        return {"access_token": "access-token", "refresh_token": "refresh-token", "token_type": "bearer"}

    monkeypatch.setattr(api_module, "authenticate_user", fake_auth)

    response = client.post(f"{api_module.API_PREFIX}/token", data={"username": "alice", "password": "secret"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"]["access_token"] == "access-token"
    assert payload["data"]["refresh_token"] == "refresh-token"
    assert payload["data"]["token_type"] == "bearer"


def test_login_endpoint_uses_authenticate_user_tokens(client, monkeypatch):
    async def fake_auth(session, username, password):
        return {"access_token": "login-access", "refresh_token": "login-refresh", "token_type": "bearer"}

    monkeypatch.setattr(api_module, "authenticate_user", fake_auth)

    response = client.post(f"{api_module.API_PREFIX}/login", data={"username": "bob", "password": "pwd"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"] == {
        "access_token": "login-access",
        "refresh_token": "login-refresh",
        "token_type": "bearer",
    }


def test_refresh_token_rejected_for_user_context(monkeypatch):
    async def fake_get_user(session, username):
        return SimpleNamespace(username=username, user_id=1)

    monkeypatch.setattr(auth_service, "get_user", fake_get_user)

    _, refresh_token = create_tokens("alice")

    async def attempt():
        with pytest.raises(InvalidTokenException):
            await auth_service.get_current_user(token=refresh_token, session=None)

    try:
        asyncio.run(attempt())
    finally:
        revoke_tokens("alice")


def test_generate_permanent_token_enforces_user_boundary(client):
    def fake_current_user():
        return SimpleNamespace(user_id=2, username="owner")

    client.app.dependency_overrides[get_current_user] = fake_current_user
    try:
        response = client.post(
            f"{api_module.API_PREFIX}/generate_permanent_token",
            params={"user_id": 1, "provider": "cli"},
        )
        assert response.status_code == 403
        payload = response.json()
        assert payload["code"] == 403
        assert payload["message"] == "Forbidden: mismatched user_id"
    finally:
        client.app.dependency_overrides.pop(get_current_user, None)


def test_refresh_token_success(client, monkeypatch):
    def fake_refresh(token):
        assert token == "valid-refresh"
        return "new-access", "new-refresh"

    monkeypatch.setattr(api_module, "refresh_access_token", fake_refresh)

    response = client.post(
        f"{api_module.API_PREFIX}/refresh",
        json={"refresh_token": "valid-refresh"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"] == {
        "access_token": "new-access",
        "token_type": "bearer",
        "refresh_token": "new-refresh",
    }


def test_refresh_token_invalid_returns_unauthorized(client, monkeypatch):
    def fake_refresh(token):
        raise InvalidTokenException(detail="Invalid refresh token")

    monkeypatch.setattr(api_module, "refresh_access_token", fake_refresh)

    response = client.post(
        f"{api_module.API_PREFIX}/refresh",
        json={"refresh_token": "invalid"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["code"] == 401
    assert payload["message"] == api_module.REFRESH_TOKEN_INVALID_MESSAGE


def test_refresh_token_revoked_returns_unauthorized(client, monkeypatch):
    def fake_refresh(token):
        raise TokenRevokedException()

    monkeypatch.setattr(api_module, "refresh_access_token", fake_refresh)

    response = client.post(
        f"{api_module.API_PREFIX}/refresh",
        json={"refresh_token": "revoked"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["code"] == 401
    assert payload["message"] == api_module.REFRESH_TOKEN_INVALID_MESSAGE
