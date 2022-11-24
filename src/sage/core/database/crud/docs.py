from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sage.core.database import models, schemas


async def get_doc_package(db: AsyncSession, name: str) -> models.DocPackage | None:
    """Get the docs that match the provided name."""
    resp = (
        await db.execute(select(models.DocPackage).where(models.DocPackage.name == name))
    ).first()
    if resp and len(resp) == 1:
        return resp[0]
    return resp


async def get_all_doc_packages(db: AsyncSession) -> list[models.DocPackage]:
    """Fetch *all* documentation packages from the database."""
    resp = (await db.execute(select(models.DocPackage))).all()
    if resp:
        return [x[0] for x in resp]
    raise Exception


async def create_doc_package(
    db: AsyncSession, doc_package: schemas.DocPackageCreationRequest
) -> models.DocPackage:
    """Create a new documentation object with the provided schema."""
    db_doc_package = models.DocPackage(
        name=doc_package.name,
        homepage=str(doc_package.homepage),
        programming_language=doc_package.programming_language,
    )
    db.add(db_doc_package, True)
    db_doc_package.id
    sources: list[models.DocSource] = []
    for source in doc_package.sources:
        # todo: use yarl for this and do validation elsewhere
        human_friendly_url = source.inventory_url.removesuffix("/objects.inv")
        sources.append(
            models.DocSource(
                package=db_doc_package,
                inventory_url=source.inventory_url,
                version=source.version,
                human_friendly_url=human_friendly_url,
                language_code=source.language,
            ),
        )
    db.add_all(sources)
    await db.commit()
    return db_doc_package
