"""Sage."""
from typing import Any, TypedDict

from fastapi import FastAPI, Request
from pydantic import BaseModel, HttpUrl


app = FastAPI(
    title="Sage",
    version="0.0.1",
    contact={
        "name": "onerandomusername",
        "url": "https://github.com/onerandomusername/sage",
    },
)


class APIContactInfo(TypedDict):
    """Represents the contact info for the api owner."""

    name: str
    url: HttpUrl


class APIMetadata(BaseModel):
    """Represents the metadata for the api itself, returned at the root of the api."""

    name: str
    version: str
    contact: APIContactInfo


@app.get("/", response_model=APIMetadata)
async def info(request: Request) -> dict[str, Any]:
    """Return the metadata for the API."""
    app: FastAPI = request.app
    return {"name": app.title, "version": app.version, "contact": app.contact}
