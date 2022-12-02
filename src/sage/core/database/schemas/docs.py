"""Pydantic Schemas for sage.core.database.models.docs."""


from pydantic import BaseModel, HttpUrl

from sage.enums import LanguageCode, ProgrammingLanguage


__all__ = (
    "DocPackage",
    "DocPackageCreationRequest",
    "DocSource",
    "DocSourceCreationRequest",
)


class DocPackageBase(BaseModel):  # noqa: D101
    name: str
    homepage: HttpUrl | None = None
    programming_language: ProgrammingLanguage


class DocPackage(DocPackageBase):
    """Represents a Documentation Package."""

    id: int
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


class DocPackageCreationRequest(DocPackageBase):
    """Payload structure to create a DocPackage."""

    # at least one source must be provided to create a package
    sources: list["DocSourceCreationWithinDocPackageCreationRequest"]

    class Config:
        schema_extra = {
            "example": {
                "name": "disnake",
                "homepage": "https://disnake.dev/",
                "programming_language": ProgrammingLanguage.python,
                "sources": [
                    {
                        "inventory_url": "https://docs.disnake.dev/en/stable/objects.inv",
                        "language": LanguageCode.en_GB,
                        "version": "2.7.0",
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
    language: LanguageCode


class DocSource(DocSourceBase):
    """Documentation Source for a Documentation Package."""

    id: int
    package: DocPackage
    preview: bool
    version: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "disnake",
                "package": DocPackage.Config.schema_extra["example"].copy(),
                "preview": False,
                "version": "2.7.0",
            }
        }


class DocSourceCreationRequest(DocSourceBase):
    """Necessary arguments to creation a Documentation Source."""

    package_id: int  # this might be a path arg, unsure
    version: str | None = None

    class Config:
        schema_extra = {
            "example": DocSource.Config.schema_extra["example"],
        }


class DocSourcePatchRequest(DocSourceBase):
    """Required parameters to change a documentation source."""

    preview: bool | None = None
    version: str | None = None


# this name is ridiculous.
# additionally, we currently don't expose documentation sources anywhere
class DocSourceCreationWithinDocPackageCreationRequest(DocSourceBase):  # noqa: D101
    version: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "inventory_url": "https://docs.disnake.dev/en/stable/objects.inv",
                "version": "2.7.0",
            }
        }


DocPackage.update_forward_refs()
DocPackageCreationRequest.update_forward_refs()
