from typing import TypedDict

from pydantic import BaseModel, HttpUrl


class APIContactInfo(TypedDict):
    """Represents the contact info for the api owner."""

    name: str
    url: HttpUrl


class APIMetadata(BaseModel):
    """Represents the metadata for the api itself, returned at the root of the api."""

    name: str
    version: str
    contact: APIContactInfo
