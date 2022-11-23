from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sage.core.database import models, schemas


async def get_docs(db: AsyncSession, name: str) -> models.DocPackage | None:
    """Get the docs that match the provided name."""
    resp = (
        await db.execute(select(models.DocPackage).where(models.DocPackage.name == name))
    ).first()
    if resp and len(resp) == 1:
        return resp[0]
    return resp


async def create_docs(
    db: AsyncSession, doc_package: schemas.DocPackageCreationRequest
) -> models.DocPackage:
    """Create a new documentation object with the provided schema."""
    db_doc_package = models.DocPackage(
        name=doc_package.name,
        is_enabled=True,
        require_opt_in=False,
        inventory_url=str(doc_package.inventory_url),
        human_url=str(doc_package.human_url),
        programming_language=doc_package.programming_language,
    )
    db.add(db_doc_package, True)
    await db.commit()
    return db_doc_package
