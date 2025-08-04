# Pydantic Settings import for environment-based configuration
from pydantic_settings import BaseSettings, SettingsConfigDict

# Application settings loaded from environment variables
class Settings(BaseSettings):
    # Configuration for the settings source (load from .env file)
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    # Database connection URL
    DATABASE_URL: str

    # Secret key used to sign JWT tokens
    SECRET_KEY: str

    # Algorithm used for JWT encoding (e.g., HS256)
    ALGORITHM: str

    # Token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int