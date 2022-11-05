import enum


__all__ = ("ProgrammingLanguage",)


class ProgrammingLanguage(enum.Enum):
    """Represents supported programming languages for documentation."""

    text = 1
    python = 2
    other = -1
