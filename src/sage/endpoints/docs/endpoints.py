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


# todo: add Depends/middleware to prevent anyone from creating a package
@router.post("/packages", response_model=schemas.DocPackage, name="Create a package")
async def post_root(
    package: schemas.DocPackageCreationRequest, db: AsyncSession = GET_SESSION
) -> schemas.DocPackage:
    """Add a new package to the documentation index."""
    async with db.begin():
        resp = await create_doc_package(db, package)
    return schemas.DocPackage.from_orm(resp)


@router.get(
    "/packages/{package_id}",
    response_model=schemas.DocPackage,
    name="Get an existing Documentation Package.",
)
async def get_package(package_id: int, db: AsyncSession = GET_SESSION) -> schemas.DocPackage:
    """Get an existing documentation package by ID."""
    async with db.begin():
        resp = await get_doc_package(db, package_id)
    return schemas.DocPackage.from_orm(resp)


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
    async with db.begin():
        resp = await modify_doc_package(db, package_id, package)
    return schemas.DocPackage.from_orm(resp)


@router.delete("/packages/{package_id}", name="Delete a package.", status_code=204)
async def delete_package(package_id: int, db: AsyncSession = GET_SESSION) -> None:
    """Delete an existing package. This cannot be undone."""
    async with db.begin():
        await delete_doc_package(db, package_id)
    return


# @router.get("/search", name="Search within package inventories")
# async def get_search(request: Request, query: str, lang: ProgrammingLanguage) -> dict[str, Any]:
#     return {}
