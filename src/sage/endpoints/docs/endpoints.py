from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from sage.core.database import schemas
from sage.core.database.crud.docs import (
    create_doc_package,
    delete_doc_package,
    get_all_doc_packages,
    get_doc_package,
    modify_doc_package,
)
from sage.core.dependencies import GET_SESSION


router = APIRouter(prefix="/docs", tags=["documentation"])


@router.get("/packages", name="Get all packages")
async def get_root(db: AsyncSession = GET_SESSION) -> list[schemas.DocPackage]:
    """Return all supported documentation inventories."""
    db_packages = await get_all_doc_packages(db)
    packages: list[schemas.DocPackage] = []
    for package in db_packages:
        packages.append(schemas.DocPackage.from_orm(package))
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
    response_model=schemas.DocPackage,
    name="Get an existing Documentation Package.",
)
async def get_package(package_id: int, db: AsyncSession = GET_SESSION) -> schemas.DocPackage:
    """Get an existing documentation package by ID."""
    resp = await get_doc_package(db, package_id)
    return schemas.DocPackage.from_orm(resp)


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


# todo: source routes to implement
# GET /packages/{package_id}/sources
# POST /packages/{package_id}/sources OR /sources
# GET /sources/{source_id}
# PATCH /sources/{source_id}
# DELETE /sources/{source_id}


# todo (much later):
# search routes and all of the different query args that will have
