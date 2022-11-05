from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from sage.core.database.models.base import Base
from sage.db import engine
from sage.endpoints import docs, meta


app = FastAPI(
    title="Sage",
    version="0.0.1",
    contact={
        "name": "onerandomusername",
        "url": "https://github.com/onerandomusername/sage",
    },
)


@app.on_event("startup")
async def startup() -> None:
    """Temporarily run migrations on api start."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# redirect root to meta
@app.get(
    "/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
    response_class=RedirectResponse,
)
async def root() -> str:
    """Redirect the user to the current root of the api."""
    return "/api/"


# we want to include no prefix on the root router
# and a prefix on the non-root router
# this means we currently serve meta from both `/` and `/api`
prefix = "/api"
app.include_router(meta.router, prefix=prefix)
app.include_router(docs.router, prefix=prefix)
