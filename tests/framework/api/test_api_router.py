import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import delete, select, text
from sqlalchemy.exc import OperationalError

from pythonprojecttemplate.api.api_router import API_PREFIX, api_router
from pythonprojecttemplate.api.auth.auth_service import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
)
from pythonprojecttemplate.api.auth.token_service import create_tokens, revoke_tokens
from pythonprojecttemplate.api.main import app
from pythonprojecttemplate.api.models.auth_models import User
from pythonprojecttemplate.api.models.result_vo import ResultVO
from pythonprojecttemplate.config.config import config
from pythonprojecttemplate.db.mysql.mysql import MySQL_Database

app.include_router(api_router)
client = TestClient(app)
expected_prefix = API_PREFIX


@asynccontextmanager
async def mysql_session():
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
        reason="数据库连接不可用，跳过API测试",
    ),
    pytest.mark.asyncio,
]


async def _clear_test_user() -> None:
    async with mysql_session() as session:
        await session.execute(delete(User).where(User.username == "testuser"))
        await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def clean_test_user():
    await _clear_test_user()
    yield
    await _clear_test_user()


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


async def get_test_token(session) -> str:
    user = await setup_test_user(session)
    access_token, _ = create_tokens(user.username)
    return access_token


async def test_api_version_and_prefix(session):
    api_config = config.get_api_config()
    expected_version = api_config.get("api_version", "v1")
    expected_prefix = f"/api/{expected_version}"

    token = await get_test_token(session)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"{expected_prefix}/test", headers=headers)
    result = ResultVO(**response.json())
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"
    assert result.code == 200
    assert result.message == "success"
    assert result.data["message"] == "Test route"
    assert result.data["version"] == expected_version
    assert result.data["user"] == "testuser"


async def test_authentication(session):
    api_config = config.get_api_config()
    expected_version = api_config.get("api_version", "v1")
    expected_prefix = f"/api/{expected_version}"

    token = await get_test_token(session)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"{expected_prefix}/test", headers=headers)
    data = response.json()["data"]
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"
    assert data["user"] == "testuser"


async def test_create_access_token():
    username = "testuser"
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data={"sub": username}, username=username, expires_delta=expires_delta)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == username
    assert "exp" in decoded


async def test_invalid_token():
    invalid_token = "invalid_token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    assert response.status_code == 401


async def test_expired_token():
    expired_token = create_access_token(
        data={"sub": "testuser"},
        username="testuser",
        expires_delta=timedelta(minutes=-1),
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    assert response.status_code == 401


async def test_unauthenticated_access():
    response = client.get(f"{expected_prefix}/test")
    assert response.status_code == 401


async def test_login_process(session):
    await setup_test_user(session)
    response = client.post(
        f"{expected_prefix}/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "success"

    data = result["data"]
    assert "access_token" in data
    assert "token_type" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_get_current_user(session):
    token = await get_test_token(session)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["user"] == "testuser"


async def test_invalid_credentials():
    response = client.post(
        f"{expected_prefix}/token",
        data={"username": "wronguser", "password": "wrongpassword"},
    )
    assert response.json()["code"] == 401
    assert response.json()["message"] == "Incorrect username or password"


async def test_invalid_token_exception():
    invalid_token = "invalid_token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


async def test_token_revoked_exception(session):
    token = await get_test_token(session)
    user = await setup_test_user(session)
    revoke_tokens(user.username)

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Token has been revoked"}


async def test_user_not_found_exception(session):
    user = await setup_test_user(session)
    access_token, _ = create_tokens(user.username)

    await session.execute(delete(User).where(User.user_id == user.user_id))
    await session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{expected_prefix}/test", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


async def test_exception_handling():
    api_config = config.get_api_config()
    expected_version = api_config.get("api_version", "v1")
    expected_prefix = f"/api/{expected_version}"

    response = client.get(f"{expected_prefix}/test_exception")
    assert response.status_code == 500

    result = response.json()
    assert "detail" in result
    assert result["detail"] == "测试异常"

