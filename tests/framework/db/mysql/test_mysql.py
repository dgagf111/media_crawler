import asyncio
from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from sqlalchemy import delete, select, text, update
from sqlalchemy.exc import OperationalError

from pythonprojecttemplate.db.mysql.mysql import MySQL_Database
from .test_table import Test_Table


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
        reason="数据库连接失败，跳过 MySQL 测试",
    ),
    pytest.mark.asyncio,
]


async def truncate_test_table(session) -> None:
    await session.execute(delete(Test_Table))
    await session.commit()


@pytest_asyncio.fixture
async def session():
    async with mysql_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_test_table(session):
    await truncate_test_table(session)
    yield
    await truncate_test_table(session)


async def test_mysql_connection(session):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1


async def test_basic_crud_operations(session):
    new_user = Test_Table(name="张三", age=30)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    assert new_user.id is not None

    result = await session.execute(select(Test_Table).where(Test_Table.id == new_user.id))
    fetched = result.scalar_one()
    assert fetched.name == "张三"
    assert fetched.age == 30

    await session.execute(
        update(Test_Table).where(Test_Table.id == new_user.id).values(age=31)
    )
    await session.commit()

    result = await session.execute(select(Test_Table).where(Test_Table.id == new_user.id))
    updated = result.scalar_one()
    assert updated.age == 31

    await session.execute(delete(Test_Table).where(Test_Table.id == new_user.id))
    await session.commit()

    result = await session.execute(select(Test_Table).where(Test_Table.id == new_user.id))
    assert result.scalar_one_or_none() is None


async def test_transaction_rollback(session):
    try:
        async with session.begin():
            user = Test_Table(name="事务测试", age=20)
            session.add(user)
            await session.flush()
            raise RuntimeError("测试回滚")
    except RuntimeError:
        pass

    result = await session.execute(select(Test_Table).where(Test_Table.name == "事务测试"))
    assert result.scalar_one_or_none() is None
