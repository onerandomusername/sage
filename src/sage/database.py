from sqlalchemy.ext.asyncio import create_async_engine

from sage.settings import get_settings


# temporary

engine = create_async_engine(get_settings().database_bind, future=True, echo=True)
