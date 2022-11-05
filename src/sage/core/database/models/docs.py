from sqlalchemy import Boolean, Column, Enum, Integer, String

from sage.core.database.models.base import Base
from sage.enums import ProgrammingLanguage


# todo: CheckConstraint for url data
class DocPackage(Base):
    """Represents a DocPackage stored in the database."""

    __tablename__ = "doc_packages"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    require_opt_in = Column(Boolean, default=True, nullable=False)
    custom_parser = Column(String(250), nullable=True)
    inventory_url = Column(String(250), nullable=True)
    human_url = Column(String(250), nullable=False)
    format_url = Column(String(250), nullable=True)
    programming_language = Column(Enum(ProgrammingLanguage), nullable=False)
    pull_request_url = Column(String(250), nullable=True)
    version_url = Column(String(250), nullable=True)

    # tags =
    # version =
