from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """
    PostgreSQL connection settings.

    All fields are read from environment variables prefixed with POSTGRES_.
    Example: POSTGRES_HOST, POSTGRES_PORT, POSTGRES_PASSWORD, ...
    """

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", env_file=".env", case_sensitive=False, extra="ignore"
    )

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    user: str = Field(default="postgres", description="Database user")
    password: SecretStr = Field(default=SecretStr("postgres"), description="Database password")
    database: str = Field(default="postgres", description="Database name")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Maximum overflow connections")

    @property
    def async_url(self) -> str:
        """Async DSN for SQLAlchemy asyncpg driver."""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.database}"
        )


database_config = DatabaseConfig()

# TODO: add separate config classes for other services (OpenAI, Redis, SMTP)
# following the same pattern: class RedisConfig(BaseSettings) with env_prefix="REDIS_"