from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from pythonprojecttemplate.config.settings import settings

# Create async engine
database_url = settings.database.url.replace("mysql+pymysql", "mysql+aiomysql")
async_engine = create_async_engine(
    database_url,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_recycle=settings.database.pool_recycle,
    pool_pre_ping=True,
    echo=settings.database.echo,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# Base for declarative models
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """异步会话上下文管理器"""
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# 保留同步接口以向后兼容（标记为废弃）
def get_legacy_session():
    """Legacy synchronous session - DEPRECATED"""
    import warnings
    warnings.warn(
        "Synchronous session is deprecated. Use async_session() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    import threading
    local = threading.local()
    if not hasattr(local, 'session'):
        local.session = AsyncSessionLocal()
    return local.session

