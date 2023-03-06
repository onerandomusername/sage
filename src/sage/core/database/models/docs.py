from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from sage.core.database.models.base import Base
from sage.enums import LanguageCode, ProgrammingLanguage


__all__ = ("DocPackage", "DocSource")


# todo: CheckConstraint for url data
class DocPackage(MappedAsDataclass, Base):
    """Represents a Package which can have multiple sources."""

    __tablename__ = "doc_packages"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    homepage: Mapped[str] = mapped_column(
        sa.String(512), nullable=False
    )  # url # not necessarily the documentation, could be pypi project page or w/e
    programming_language: Mapped[ProgrammingLanguage] = mapped_column(
        sa.Enum(ProgrammingLanguage), nullable=False
    )

    sources: Mapped[list["DocSource"]] = relationship(
        "DocSource", cascade="all, delete, delete-orphan"
    )

    def to_dict(self, include_sources: bool = False) -> dict[str, Any]:
        """Convert the package to a dict representation which is ready for json serialisation."""
        resp: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "homepage": self.homepage,
            "programming_language": self.programming_language,
        }
        if include_sources:
            # note: this requires await or cached
            resp["sources"] = [source.to_dict(include_package=False) for source in self.sources]
        return resp


class DocSource(Base):
    """Represents a documentation source for a specific version/language of a DocPackage."""

    __tablename__ = "doc_sources"
    __table_args__ = (
        sa.Index(
            "ix_doc_source_defaults",
            "package_id",
            "default",
            unique=True,
            postgresql_where=sa.Column("default"),
        ),
    )

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    package: Mapped[DocPackage] = relationship("DocPackage", back_populates="sources")
    package_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("doc_packages.id", ondelete="CASCADE", name="doc_sources_package_id_fkey"),
        nullable=False,
    )
    preview: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    default: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    inventory_url: Mapped[str] = mapped_column(sa.String(250), nullable=True)
    human_friendly_url: Mapped[str] = mapped_column(sa.String(250), nullable=False)
    version: Mapped[str] = mapped_column(sa.String(30), nullable=True)
    language_code: Mapped[LanguageCode] = mapped_column(sa.Enum(LanguageCode), nullable=False)

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
