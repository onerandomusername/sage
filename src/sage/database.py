from sqlalchemy.ext.asyncio import create_async_engine

from sage.settings import SETTINGS


# temporary

engine = create_async_engine(SETTINGS.database_bind, future=True, echo=True)
