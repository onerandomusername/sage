"""Pydantic Schemas for sage.core.database.models.docs."""
from pydantic import BaseModel, HttpUrl

from sage.enums import ProgrammingLanguage


__all__ = ("DocPackage", "DocPackageCreate")


class DocPackageBase(BaseModel):
    name: str
    inventory_url: HttpUrl
    human_url: HttpUrl
    programming_language: ProgrammingLanguage


class DocPackageCreate(DocPackageBase):
    """Payload structure to create a DocPackage."""

    class Config:
        schema_extra = {
            "example": dict(
                name="disnake",
                inventory_url="https://docs.disnake.dev/en/stable/objects.inv",
                human_url="https://docs.disnake.dev/en/stable/",
                programming_language=ProgrammingLanguage.python,
            )
        }


class DocPackage(DocPackageBase):
    """Represents a Documentation Package."""

    is_enabled: bool = True
    # require_opt_in:bool = False
    # custom_parser:str|None = None
    # pull_request_url: HttpUrl|None = None
    # version_url: HttpUrl|None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": dict(
                name="disnake",
                inventory_url="https://docs.disnake.dev/en/stable/objects.inv",
                human_url="https://docs.disnake.dev/en/stable/",
                programming_language=ProgrammingLanguage.python,
                is_enabled=True,
            )
        }
