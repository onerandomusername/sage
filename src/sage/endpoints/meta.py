from typing import Any

from fastapi import APIRouter, FastAPI, Request

from sage.core.models.meta import APIMetadata


router = APIRouter(tags=["meta"])


@router.get("/", response_model=APIMetadata)
async def info(request: Request) -> dict[str, Any]:
    """Return the metadata for the API."""
    app: FastAPI = request.app
    return {"name": app.title, "version": app.version, "contact": app.contact}
