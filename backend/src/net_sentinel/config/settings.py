from pydantic import AliasChoices, Field, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = None
    redis_dsn: RedisDsn = Field(
        default=RedisDsn("redis://localhost:6379"),
        validation_alias=AliasChoices("service_redis_dsn", "redis_url"),
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @model_validator(mode="after")
    def set_default(self) -> "Settings":
        if not self.DATABASE_URL:
            self.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
        return self


settings = Settings()
