from fastapi import APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession

from sage.core.database import schemas
from sage.core.database.crud.docs import create_docs
from sage.core.dependencies import GET_SESSION
from sage.enums import ProgrammingLanguage


router = APIRouter(prefix="/docs", tags=["documentation"])


@router.get("/", name="Get all packages")
async def get_root(
    request: Request, lang: ProgrammingLanguage = ProgrammingLanguage.python
) -> dict[str, list[schemas.DocPackage]]:
    """Return all supported documentation inventories."""
    # for now return mock data
    return {
        lang.value: [
            schemas.DocPackage(
                name="python",
                inventory_url="https://docs.python.org/3/objects.inv",  # type: ignore
                human_url="https://docs.python.org/3/",  # type: ignore
                programming_language=lang,
            ),
            schemas.DocPackage(
                name="disnake",
                inventory_url="https://docs.disnake.dev/page/objects.inv",  # type: ignore
                human_url="https://docs.disnake.dev/page/",  # type: ignore
                programming_language=lang,
            ),
        ]
    }


# todo: add Depends/middleware to prevent anyone from creating a package
@router.post("/", response_model=schemas.DocPackage, name="Create a package")
async def post_root(
    package: schemas.DocPackageCreationRequest, db: AsyncSession = GET_SESSION
) -> schemas.DocPackage:
    """Add a new package to the documentation index."""
    async with db.begin():
        resp = await create_docs(db, package)
    return schemas.DocPackage.from_orm(resp)


# @router.get("/search", name="Search within package inventories")
# async def get_search(request: Request, query: str, lang: ProgrammingLanguage) -> dict[str, Any]:
#     return {}
