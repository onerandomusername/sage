# Dependency

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from sage.db import engine


SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False, future=True, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get the database to be used in a route callback."""
    db: AsyncSession = SessionLocal()  # type: ignore
    try:
        yield db
    finally:
        await db.close()


GET_DB = Depends(get_db)
