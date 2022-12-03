from fastapi import HTTPException
from sqlalchemy import delete, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from sage.core.database import models, schemas


async def get_doc_package(
    db: AsyncSession, id: int, *, include_sources: bool = False
) -> models.DocPackage | None:
    """Get the docs by their primary key."""
    stmt = (
        select(models.DocPackage)
        .options(selectinload(models.DocPackage.sources))
        .where(models.DocPackage.id == id)
    )
    try:
        resp = (await db.execute(stmt)).one()
    except NoResultFound:
        return None
    if resp and len(resp) == 1:
        return resp[0]
    return resp


async def get_doc_package_by_name(db: AsyncSession, name: str) -> models.DocPackage | None:
    """Get the docs that match the provided name."""
    resp = (await db.execute(select(models.DocPackage).where(models.DocPackage.name == name))).one()
    if resp and len(resp) == 1:
        return resp[0]
    return resp


async def get_all_doc_packages(db: AsyncSession) -> list[models.DocPackage]:
    """Fetch *all* documentation packages from the database."""
    resp = (await db.execute(select(models.DocPackage))).all()
    if not resp:
        # todo: make more specific
        raise Exception
    return [row[0] for row in resp]


async def create_doc_package(
    db: AsyncSession, doc_package: schemas.DocPackageCreationRequest
) -> models.DocPackage:
    """Create a new documentation object with the provided schema."""
    db_doc_package = models.DocPackage(
        name=doc_package.name,
        homepage=str(doc_package.homepage),
        programming_language=doc_package.programming_language,
    )
    async with db.begin():
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
                    language_code=source.language_code,
                ),
            )
        db.add(db_doc_package, True)
        db.add_all(sources)
        await db.commit()
    return db_doc_package


async def modify_doc_package(
    db: AsyncSession, id: int, doc_package: schemas.DocPackagePatchRequest
) -> models.DocPackage:
    """Modify the existing doc_package with the newly provided request."""
    stmt = (
        update(models.DocPackage)
        .where(models.DocPackage.id == id)
        .values(**doc_package.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    async with db.begin():
        result: CursorResult = await db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No package with id '{id}' was found.")
        if result.rowcount != 1:
            await db.rollback()
            raise RuntimeError(
                "updated more than one package based on primary key. This code is unreachable."
            )
        # fetch the new package
        package = await get_doc_package(db, id)
        await db.commit()
    return package


async def delete_doc_package(
    db: AsyncSession,
    id: int,
) -> None:
    """Delete documentation package based on ID."""
    stmt = delete(models.DocPackage).where(models.DocPackage.id == id)
    async with db.begin():
        result: CursorResult = await db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No package with id '{id}' was found.")
        if result.rowcount != 1:
            await db.rollback()
            raise RuntimeError(
                "deleted more than one package based on primary key. This code is unreachable."
            )
        await db.commit()
    return


async def get_doc_source(db: AsyncSession, id: int) -> models.DocSource | None:
    """Get a source by id."""
    stmt = (
        select(models.DocSource)
        .options(selectinload(models.DocSource.package))
        .where(models.DocSource.id == id)
    )
    try:
        resp = (await db.execute(stmt)).one()
    except NoResultFound:
        return None
    if resp and len(resp) == 1:
        return resp[0]
    return resp


async def get_all_sources_for_package(db: AsyncSession, package_id: int) -> list[models.DocSource]:
    """Get all sources for a specific package."""
    stmt = select(models.DocSource).where(models.DocSource.package_id == package_id)
    resp = await db.execute(stmt)
    if not resp:
        # todo: make more specific
        raise Exception
    return [row[0] for row in resp]


async def create_doc_source(
    db: AsyncSession, doc_source: schemas.DocSourceCreationRequest
) -> models.DocPackage:
    """Create a documentation source using the package_id provided in the request."""
    package_id = doc_source.package_id

    async with db.begin():
        # validate the package exists
        doc_package = await get_doc_package(db, package_id)
        if not doc_package:
            raise HTTPException(400, "documentation package does not exist")

        human_friendly_url = doc_source.inventory_url.removesuffix("/objects.inv")

        db_doc_source = models.DocSource(
            package_id=package_id,
            inventory_url=doc_source.inventory_url,
            version=doc_source.version,
            human_friendly_url=human_friendly_url,
            language_code=doc_source.language_code,
        )
        db.add(db_doc_source, True)
        await db.commit()
    return db_doc_source


async def modify_doc_source(
    db: AsyncSession, id: int, doc_source: schemas.DocSourcePatchRequest
) -> schemas.DocSource:
    """Modify the provided source."""
    stmt = (
        update(models.DocSource)
        .where(models.DocSource.id == id)
        .values(**doc_source.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    async with db.begin():
        result: CursorResult = await db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No source with id '{id}' was found.")
        if result.rowcount != 1:
            await db.rollback()
            raise RuntimeError(
                "updated more than one source based on primary key. This code is unreachable."
            )
        # fetch the new package
        source = await get_doc_source(db, id)
        await db.commit()
    return source


async def delete_doc_source(
    db: AsyncSession,
    id: int,
) -> None:
    """Delete documentation source based on ID."""
    stmt = delete(models.DocSource).where(models.DocSource.id == id)
    async with db.begin():
        result: CursorResult = await db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No source with id '{id}' was found.")
        if result.rowcount != 1:
            await db.rollback()
            raise RuntimeError(
                "deleted more than one source based on primary key. This code is unreachable."
            )
        await db.commit()
    return
