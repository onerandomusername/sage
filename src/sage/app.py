from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from sage.endpoints import docs, meta
from sage.logging import configure_logging


app = FastAPI(
    title="Sage",
    version="0.0.1",
    contact={
        "name": "onerandomusername",
        "url": "https://github.com/onerandomusername/sage",
    },
)


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


@app.on_event("startup")
async def setup_logging() -> None:
    """Configure logging on application startup."""
    configure_logging()


# we want to include no prefix on the root router
# and a prefix on the non-root router
# this means we currently serve meta from both `/` and `/api`
prefix = "/api"
app.include_router(meta.router, prefix=prefix)
app.include_router(docs.router, prefix=prefix)
