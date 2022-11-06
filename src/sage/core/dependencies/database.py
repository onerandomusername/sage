# Dependency

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from sage.database import engine


SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False, future=True, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database to be used in a route callback."""
    session: AsyncSession = SessionLocal()  # type: ignore
    try:
        yield session
    finally:
        await session.close()


GET_SESSION = Depends(get_session)
