from pydantic import BaseSettings, Field, PostgresDsn


__all__ = ("Settings", "get_settings")


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {
        "postgresql+asyncpg",
    }


class Settings(BaseSettings):
    """The main configuration for Sage."""

    database_bind: AsyncPostgresDsn = Field(env="SAGE_DATABASE_BIND")
    debug: bool = False

    class Config:  # noqa: D106
        env_prefix = "SAGE_"


_SETTINGS = None


def get_settings() -> Settings:
    """Get the global configuration instance. This allows for lazy fetching."""
    global _SETTINGS
    if _SETTINGS is None:
        _SETTINGS = Settings()  # type: ignore # these are filled by env vars
    return _SETTINGS
