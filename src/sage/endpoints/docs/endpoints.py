from typing import Any

from fastapi import APIRouter, HTTPException
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


@router.get("/packages", name="Get all packages")
async def get_root(db: AsyncSession = GET_SESSION) -> list[dict[str, Any]]:
    """Return all supported documentation inventories."""
    db_packages = await get_all_doc_packages(db)
    packages: list[dict[str, Any]] = []
    for package in db_packages:
        packages.append(package.to_dict())
    return packages


# todo: add Depends/middleware to make this admin only
@router.post("/packages", response_model=schemas.DocPackage, name="Create a package")
async def post_root(
    package: schemas.DocPackageCreationRequest, db: AsyncSession = GET_SESSION
) -> schemas.DocPackage:
    """Add a new package to the documentation index."""
    resp = await create_doc_package(db, package)
    return schemas.DocPackage.from_orm(resp)


@router.get(
    "/packages/{package_id}",
    name="Get an existing Documentation Package.",
)
async def get_package(package_id: int, db: AsyncSession = GET_SESSION) -> dict[str, Any]:
    """Get an existing documentation package by ID."""
    resp = await get_doc_package(db, package_id)
    if resp is None:
        raise HTTPException(404, "Package could not be found.")
    return resp.to_json(include_sources=True)


# todo: add Depends/middleware to make this admin only
@router.patch(
    "/packages/{package_id}",
    response_model=schemas.DocPackage,
    name="Modify an existing DocPackage",
)
async def modify_package(
    package_id: int,
    package: schemas.DocPackagePatchRequest,
    db: AsyncSession = GET_SESSION,
) -> schemas.DocPackage:
    """Modify an existing Package. The full package must be provided."""
    resp = await modify_doc_package(db, package_id, package)
    return schemas.DocPackage.from_orm(resp)


# todo: add Depends/middleware to prevent anyone from creating a package
@router.delete("/packages/{package_id}", name="Delete a package.", status_code=204)
async def delete_package(package_id: int, db: AsyncSession = GET_SESSION) -> None:
    """Delete an existing package. This cannot be undone."""
    await delete_doc_package(db, package_id)
    return


@router.get("/packages/{package_id}/sources", name="Get package sources")
async def get_package_sources(
    package_id: int, db: AsyncSession = GET_SESSION
) -> list[models.DocSource]:
    """Show all sources for a specific package."""
    db_sources = await get_all_sources_for_package(db, package_id)
    return db_sources


@router.post("/sources", name="create a new package source")
async def create_package_source(
    source: schemas.DocSourceCreationRequest, db: AsyncSession = GET_SESSION
) -> models.DocSource:
    """Create a new source for a package."""
    db_source = await create_doc_source(db, source)
    return db_source


@router.get("/sources/{source_id}")
async def show_source(source_id: int, db: AsyncSession = GET_SESSION) -> dict[str, Any]:
    """Get information on the provided source number."""
    resp = await get_doc_source(db, source_id)
    if not resp:
        raise HTTPException(404, "The source could not be found.")
    return resp.to_dict(include_package=True)


@router.patch("/sources/{source_id}")
async def modify_source(
    source_id: int, source: schemas.DocSourcePatchRequest, db: AsyncSession = GET_SESSION
) -> schemas.DocSource:
    """Modify the provided source. This will fully replace the last source."""
    new_source = await modify_doc_source(db, source_id, source)
    return new_source


@router.delete("/sources/{source_id}", status_code=204)
async def delete_source(source_id: int, db: AsyncSession = GET_SESSION) -> None:
    """Delete the provided source by ID."""
    await delete_doc_source(db, source_id)
    return


# todo (much later):
# search routes and all of the different query args that will have
