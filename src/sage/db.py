from sqlalchemy.ext.asyncio import create_async_engine


# temporary
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
