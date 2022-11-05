import enum


__all__ = ("ProgrammingLanguage",)


class ProgrammingLanguage(enum.Enum):
    """Represents supported programming languages for documentation."""

    python = "python"
    text = "text-only"
    other = "other"
