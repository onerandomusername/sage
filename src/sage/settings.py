from pydantic import BaseSettings, Field, PostgresDsn


__all__ = ("SETTINGS",)


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {
        "postgresql+asyncpg",
    }


class Settings(BaseSettings):
    database_bind: AsyncPostgresDsn = Field(env="SAGE_DATABASE_BIND")
    debug: bool = False

    class Config:
        env_prefix = "SAGE_"


SETTINGS = Settings()  # type: ignore # these parameters are provided by the environment
