from typing import Any

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from sage.core.database import models, schemas
from sage.core.database.crud.docs import (
    create_doc_package,
    create_doc_source,
    delete_doc_package,
    delete_doc_source,
    get_all_doc_packages,
    get_all_sources_for_package,
    get_doc_package,
    get_doc_source,
    modify_doc_package,
    modify_doc_source,
)
from sage.core.dependencies import GET_SESSION


router = APIRouter(prefix="/docs", tags=["documentation"])

common_package_responses: dict[str | int, dict[str, Any]] = {
    404: {
        "description": "The package could not be found.",
        "content": {
            "application/json": {"message": {"detail": "No package with id '0' was found."}}
        },
    }
}
common_source_responses: dict[str | int, dict[str, Any]] = {
    404: {
        "description": "The source could not be found.",
        "content": {
            "application/json": {"message": {"detail": "No source with id '0' was found."}}
        },
    }
}


@router.get("/packages", name="Get all packages", responses=common_package_responses)
async def get_root(db: AsyncSession = GET_SESSION) -> list[dict[str, Any]]:
    """Return all supported documentation inventories."""
    db_packages = await get_all_doc_packages(db)
    packages: list[dict[str, Any]] = []
    for package in db_packages:
        packages.append(package.to_dict())
    return packages


# todo: add Depends/middleware to make this admin only
@router.post(
    "/packages",
    # response_model=schemas.DocPackage,
    # response_model_exclude={"sources": {"__all__": {"package"}}},
    name="Create a package",
    status_code=201,
    responses={**common_package_responses, 201: {"description": "Package successfully created"}},
)
async def post_root(
    package: schemas.DocPackageCreationRequest, db: AsyncSession = GET_SESSION
) -> dict[str, Any]:
    """Add a new package to the documentation index."""
    db_package = await create_doc_package(db, package)
    return db_package.to_dict(include_sources=True)


@router.get(
    "/packages/{package_id}",
    name="Get an existing Documentation Package.",
    responses=common_package_responses,
)
async def get_package(
    package_id: int = Path(ge=0, lt=1 << 31), db: AsyncSession = GET_SESSION  # noqa: B008
) -> dict[str, Any]:
    """Get an existing documentation package by ID."""
    resp = await get_doc_package(db, package_id)
    if resp is None:
        raise HTTPException(404, "Package could not be found.")
    return resp.to_dict(include_sources=True)


# todo: add Depends/middleware to make this admin only
@router.patch(
    "/packages/{package_id}",
    # response_model=schemas.DocPackage,
    name="Modify an existing DocPackage",
    responses=common_package_responses,
)
async def modify_package(
    package: schemas.DocPackagePatchRequest,
    package_id: int = Path(ge=0, lt=1 << 31),  # noqa: B008
    db: AsyncSession = GET_SESSION,
) -> dict[str, Any]:
    """Modify an existing Package. The full package must be provided."""
    resp = await modify_doc_package(db, package_id, package)
    return resp.to_dict(include_sources=False)


# todo: add Depends/middleware to prevent anyone from creating a package
@router.delete(
    "/packages/{package_id}",
    name="Delete a package.",
    responses={
        **common_package_responses,
        204: {"description": "Package deletion was a success"},
    },
)
async def delete_package(
    package_id: int = Path(ge=0, lt=1 << 31), db: AsyncSession = GET_SESSION  # noqa: B008
) -> None:
    """Delete an existing package. This cannot be undone."""
    await delete_doc_package(db, package_id)
    return


@router.get(
    "/packages/{package_id}/sources", name="Get package sources", responses=common_source_responses
)
async def get_package_sources(
    package_id: int = Path(ge=0, lt=1 << 31), db: AsyncSession = GET_SESSION  # noqa: B008
) -> list[models.DocSource]:
    """Show all sources for a specific package."""
    db_sources = await get_all_sources_for_package(db, package_id)
    return db_sources


@router.post(
    "/sources",
    name="create a new package source",
    responses={
        **common_source_responses,
        400: {"description": "The documentation package does not exist."},
    },
    status_code=201,
)
async def create_package_source(
    source: schemas.DocSourceCreationRequest, db: AsyncSession = GET_SESSION
) -> models.DocSource:
    """Create a new source for a package."""
    db_source = await create_doc_source(db, source)
    return db_source


@router.get("/sources/{source_id}", responses=common_source_responses)
async def show_source(
    source_id: int = Path(ge=0, lt=1 << 31), db: AsyncSession = GET_SESSION  # noqa: B008
) -> dict[str, Any]:
    """Get information on the provided source number."""
    resp = await get_doc_source(db, source_id)
    if not resp:
        raise HTTPException(404, "The source could not be found.")
    return resp.to_dict(include_package=True)


@router.patch("/sources/{source_id}", responses=common_source_responses)
async def modify_source(
    source: schemas.DocSourcePatchRequest,
    source_id: int = Path(ge=0, lt=1 << 31),  # noqa: B008
    db: AsyncSession = GET_SESSION,
) -> schemas.DocSource:
    """Modify the provided source. This will fully replace the last source."""
    new_source = await modify_doc_source(db, source_id, source)
    return new_source


@router.delete(
    "/sources/{source_id}",
    responses={
        **common_source_responses,
        204: {"description": "Source deletion was a success"},
    },
)
async def delete_source(
    source_id: int = Path(ge=0, lt=1 << 31), db: AsyncSession = GET_SESSION  # noqa: B008
) -> None:
    """Delete the provided source by ID."""
    await delete_doc_source(db, source_id)
    return


# todo (much later):
# search routes and all of the different query args that will have
