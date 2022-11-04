"""Sage."""

from fastapi import FastAPI

from sage.endpoints import root


app = FastAPI(
    title="Sage",
    version="0.0.1",
    contact={
        "name": "onerandomusername",
        "url": "https://github.com/onerandomusername/sage",
    },
)

app.include_router(root.router)
