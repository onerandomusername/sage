from pydantic import BaseSettings, Field, PostgresDsn, SecretBytes


__all__ = ("Settings", "get_settings")


class AsyncPostgresDsn(PostgresDsn):  # noqa: D101
    allowed_schemes = {
        "postgresql+asyncpg",
    }


class AdminSettings(BaseSettings):
    """Admin account settings."""

    username: bytes
    password: SecretBytes

    class Config:  # noqa: D106
        env_prefix = "SAGE_ADMIN_"


class Settings(BaseSettings):
    """The main configuration for Sage."""

    database_bind: AsyncPostgresDsn = Field(env="SAGE_DATABASE_BIND")
    debug: bool = False
    admin: AdminSettings = AdminSettings()  # type: ignore # these are filled by env vars

    class Config:  # noqa: D106
        env_prefix = "SAGE_"


_SETTINGS = None


def get_settings() -> Settings:
    """Get the global configuration instance. This allows for lazy fetching."""
    global _SETTINGS
    if _SETTINGS is None:
        _SETTINGS = Settings()  # type: ignore # these are filled by env vars
    return _SETTINGS
