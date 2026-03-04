from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str 

    # Redis
    REDIS_URL: str 

    # JWT
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str
    JWT_EXPIRY_HOURS: int 

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str 
    GOOGLE_REDIRECT_URI: str 

    # App
    APP_ENV: str 
    APP_HOST: str
    APP_PORT: int 

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int 

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def sync_database_url(self) -> str:
        """Return a synchronous database URL for Alembic."""
        return self.DATABASE_URL.replace("+asyncpg", "+psycopg2")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
