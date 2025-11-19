from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from pythonprojecttemplate.db.session import Base, async_engine, AsyncSessionLocal


MySQL_Base = Base


class MySQL_Database:
    """
    Database helper for async operations.
    """

    def __init__(self):
        self.engine = async_engine
        self.Session = AsyncSessionLocal

    async def get_session(self):
        """Get an async database session"""
        async with self.Session() as session:
            yield session

    def close_session(self):
        """Close session (handled by async context manager)"""
        pass
