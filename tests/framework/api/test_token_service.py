import asyncio
import time
from contextlib import asynccontextmanager
from datetime import timedelta

import pytest
import pytest_asyncio
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import delete, select, text
from sqlalchemy.exc import OperationalError

from pythonprojecttemplate.api.api_router import API_PREFIX, api_router
from pythonprojecttemplate.api.auth.auth_service import (
    ALGORITHM,
    SECRET_KEY,
    get_password_hash,
)
from pythonprojecttemplate.api.auth.token_service import (
    create_tokens,
    refresh_access_token,
    revoke_tokens,
    verify_token,
)
from pythonprojecttemplate.api.main import app
from pythonprojecttemplate.api.models.auth_models import ThirdPartyToken, User
from pythonprojecttemplate.db.mysql.mysql import MySQL_Database

app.include_router(api_router)
client = TestClient(app)
expected_prefix = API_PREFIX


@asynccontextmanager
async def mysql_session():
    """统一的异步 MySQL 会话上下文，简化测试中的 session 管理。"""
    db = MySQL_Database()
    session_gen = db.get_session()
    session = await session_gen.__anext__()
    try:
        yield session
    finally:
        try:
            await session.rollback()
        finally:
            await session_gen.aclose()


async def _ping_database() -> None:
    async with mysql_session() as session:
        await session.execute(text("SELECT 1"))


def check_database_connection() -> bool:
    try:
        asyncio.run(_ping_database())
        return True
    except OperationalError:
        return False
    except Exception:
        return False


pytestmark = [
    pytest.mark.skipif(
        not check_database_connection(),
        reason="数据库连接不可用，跳过令牌服务测试",
    ),
    pytest.mark.asyncio,
]


async def _clear_test_records() -> None:
    async with mysql_session() as session:
        await session.execute(delete(ThirdPartyToken))
        await session.execute(delete(User).where(User.username == "testuser"))
        await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def clean_test_records():
    await _clear_test_records()
    yield
    await _clear_test_records()


@pytest_asyncio.fixture
async def session():
    async with mysql_session() as session:
        yield session


async def setup_test_user(session) -> User:
    result = await session.execute(select(User).where(User.username == "testuser"))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        return existing_user

    hashed_password = get_password_hash("testpassword")
    user = User(username="testuser", password_hash=hashed_password, email="test@example.com")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def test_create_tokens(session):
    user = await setup_test_user(session)
    access_token, refresh_token = create_tokens(user.username)

    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user.username
    assert "exp" in payload

    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user.username
    assert payload["type"] == "refresh"
    assert "exp" in payload


async def test_refresh_access_token(session):
    user = await setup_test_user(session)
    _, refresh_token = create_tokens(user.username)

    new_access_token, new_refresh_token = refresh_access_token(refresh_token)

    payload = jwt.decode(new_access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user.username
    assert "exp" in payload

    payload = jwt.decode(new_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user.username
    assert payload["type"] == "refresh"
    assert "exp" in payload


async def test_revoke_tokens(session):
    user = await setup_test_user(session)
    access_token, _ = create_tokens(user.username)

    revoke_tokens(user.username)

    response = client.get(
        f"{expected_prefix}/test", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.json()}"


async def test_verify_token(session):
    user = await setup_test_user(session)
    access_token, _ = create_tokens(user.username)

    payload = verify_token(access_token)
    assert payload["sub"] == user.username


async def test_verify_expired_token():
    payload = {"sub": "testuser", "exp": int(time.time()) - 300}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        verify_token(token)
    assert excinfo.value.status_code == 401


async def test_login_and_refresh_flow(session):
    user = await setup_test_user(session)
    access_token, refresh_token = create_tokens(user.username)

    response = client.get(
        f"{expected_prefix}/test", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"

    new_access_token, _ = refresh_access_token(refresh_token)
    response = client.get(
        f"{expected_prefix}/test", headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"


async def test_logout(session):
    await setup_test_user(session)
    response = client.post(
        f"{expected_prefix}/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"

    tokens = response.json()["data"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.post(f"{expected_prefix}/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

