from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from sage.core.database import schemas
from sage.core.database.crud.docs import create_doc_package, get_all_doc_packages
from sage.core.dependencies import GET_SESSION


router = APIRouter(prefix="/docs", tags=["documentation"])


@router.get("/", name="Get all packages")
async def get_root(db: AsyncSession = GET_SESSION) -> list[schemas.DocPackage]:
    """Return all supported documentation inventories."""
    db_packages = await get_all_doc_packages(db)
    packages: list[schemas.DocPackage] = []
    for package in db_packages:
        packages.append(schemas.DocPackage.from_orm(package))
    return packages


# todo: add Depends/middleware to prevent anyone from creating a package
@router.post("/", response_model=schemas.DocPackage, name="Create a package")
async def post_root(
    package: schemas.DocPackageCreationRequest, db: AsyncSession = GET_SESSION
) -> schemas.DocPackage:
    """Add a new package to the documentation index."""
    async with db.begin():
        resp = await create_doc_package(db, package)
    return schemas.DocPackage.from_orm(resp)


# @router.get("/search", name="Search within package inventories")
# async def get_search(request: Request, query: str, lang: ProgrammingLanguage) -> dict[str, Any]:
#     return {}
