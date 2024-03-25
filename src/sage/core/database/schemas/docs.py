"""Pydantic Schemas for sage.core.database.models.docs."""

from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

from sage.enums import LanguageCode, ProgrammingLanguage


__all__ = (
    "DocPackage",
    "DocPackageCreationRequest",
    "DocSource",
    "DocSourceCreationRequest",
)


class DocPackageBase(BaseModel):  # noqa: D101
    name: str = Field(min_length=0, max_length=100, regex="^[a-z0-9A-Z.-_]+$")
    homepage: HttpUrl | None = None
    programming_language: ProgrammingLanguage


class DocPackage(DocPackageBase):
    """Represents a Documentation Package."""

    id: int = Field(ge=0, lt=1 << 31)
    sources: list["DocSource"]

    class Config:

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "disnake",
                "homepage": "https://disnake.dev/",
                "programming_language": ProgrammingLanguage.python,
                "sources": [
                    {
                        "inventory_url": "https://docs.disnake.dev/en/stable/objects.inv",
                        "preview": False,
                        "version": "2.7.0",
                        "language_code": LanguageCode.en_GB,
                    }
                ],
            }
        }


class DocPackagePatchRequest(DocPackageBase):
    """Represents a Documentation Package."""

    # sources: list["DocSource"]

    class Config:
        schema_extra = {
            "example": {
                "name": "disnake 2.0",
                "homepage": "https://disnake.dev/?",
                "programming_language": ProgrammingLanguage.text,
                "sources": [
                    {
                        "inventory_url": "https://docs.disnake.dev/en/latest/objects.inv",
                        "preview": False,
                        "version": "2.8.0a",
                        "language_code": LanguageCode.en_GB,
                    }
                ],
            }
        }


class DocSourceBase(BaseModel):  # noqa: D101
    inventory_url: HttpUrl
    language_code: LanguageCode


class DocSource(DocSourceBase):
    """Documentation Source for a Documentation Package."""

    id: int = Field(ge=0, lt=1 << 31)
    package: DocPackage
    default: bool
    preview: bool
    version: str = Field(regex="^[a-z0-9A-Z.-_]+$")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "disnake",
                "package": DocPackage.Config.schema_extra["example"].copy(),
                "inventory_url": "https://docs.disnake.dev/en/v2.7.0/objects.inv",
                "preview": False,
                "version": "2.7.0",
            }
        }


class DocSourceCreationRequest(DocSourceBase):
    """Necessary arguments to creation a Documentation Source."""

    package_id: int = Field(ge=0, lt=1 << 31)  # this might be a path arg, unsure
    default: bool = False
    version: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "inventory_url": "https://docs.disnake.dev/en/v2.7.0/objects.inv",
                "version": "2.7.0",
                "package_id": 12,
                "default": False,
                "language_code": LanguageCode.en_US,
            },
        }


class DocSourcePatchRequest(DocSourceBase):
    """Required parameters to change a documentation source."""

    preview: bool | None = None
    version: str | None = Field(regex="^[0-9a-zA-Z-.]$")


# this name is ridiculous.
class DocSourceCreationWithinDocPackageCreationRequest(DocSourceBase):  # noqa: D101
    version: str | None = None
    default: bool = False

    class Config:
        schema_extra = {
            "example": {
                "inventory_url": "https://docs.disnake.dev/en/stable/objects.inv",
                "version": "2.7.0",
            }
        }


class DocPackageCreationRequest(DocPackageBase):
    """Payload structure to create a DocPackage."""

    # at least one source must be provided to create a package
    sources: Annotated[list[DocSourceCreationWithinDocPackageCreationRequest], Field(min_items=1)]

    class Config:
        schema_extra = {
            "example": {
                "name": "disnake",
                "homepage": "https://disnake.dev/",
                "programming_language": ProgrammingLanguage.python,
                "sources": [
                    {
                        "inventory_url": "https://docs.disnake.dev/en/stable/objects.inv",
                        "language_code": LanguageCode.en_GB,
                        "version": "2.7.0",
                    }
                ],
            }
        }


DocPackage.update_forward_refs()
DocPackageCreationRequest.update_forward_refs()
DocSourceCreationWithinDocPackageCreationRequest.update_forward_refs()
