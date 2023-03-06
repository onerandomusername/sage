# Dependency

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sage.database import engine


SessionLocal = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database to be used in a route callback."""
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


GET_SESSION = Depends(get_session)
