from typing import Any

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sage.core.database.models.base import Base
from sage.enums import LanguageCode, ProgrammingLanguage


__all__ = ("DocPackage", "DocSource")


# todo: CheckConstraint for url data
class DocPackage(Base):
    """Represents a Package which can have multiple sources."""

    __tablename__ = "doc_packages"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    homepage = Column(
        String(512), nullable=False
    )  # url # not necessarily the documentation, could be pypi project page or w/e
    programming_language = Column(Enum(ProgrammingLanguage), nullable=False)

    sources = relationship("DocSource", cascade="all, delete, delete-orphan")

    def to_dict(self, include_sources: bool = False) -> dict[str, Any]:
        """Convert the package to a dict representation which is ready for json serialisation."""
        resp = {
            "id": self.id,
            "name": self.name,
            "homepage": self.homepage,
            "programming_language": self.programming_language,
        }
        if include_sources:
            # note: this requires await or cached
            resp["sources"] = self.sources
        return resp


class DocSource(Base):
    """Represents a documentation source for a specific version/language of a DocPackage."""

    __tablename__ = "doc_sources"

    id = Column(Integer, primary_key=True)
    package = relationship("DocPackage", back_populates="sources")
    package_id = Column(Integer, ForeignKey("doc_packages.id", ondelete="CASCADE"))
    preview = Column(Boolean, default=True, nullable=False)
    inventory_url = Column(String(250), nullable=True)
    human_friendly_url = Column(String(250), nullable=False)
    version = Column(String(30), nullable=True)
    language_code = Column(Enum(LanguageCode), nullable=False)

    def to_dict(self, include_package: bool = False) -> dict[str, Any]:
        """Convert the source to a dict representation which is ready for json serialisation."""
        resp = {
            "id": self.id,
            "package_id": self.package_id,
            "preview": self.preview,
            "inventory_url": self.inventory_url,
            "human_friendly_url": self.human_friendly_url,
            "version": self.version,
            "language_code": self.language_code,
        }
        if include_package:
            # note: this requires await or cached
            resp["package"] = self.package
        return resp
