"""
Centralized configuration via pydantic-settings.
All env vars are validated at startup — fail fast on misconfiguration.
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- App ---
    APP_NAME: str = "AstraBlock"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # production | staging | development

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 1
    ALLOWED_HOSTS: List[str] = ["*"]

    # --- CORS ---
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # --- Security ---
    ADMIN_API_KEY: Optional[str] = None
    API_KEY_HEADER: str = "X-API-Key"
    RATE_LIMIT_CALLS: int = 120
    RATE_LIMIT_PERIOD: int = 60

    # --- Database ---
    APIKEY_DB_PATH: str = "./data/apikeys.db"

    # --- External APIs ---
    ETHERSCAN_API_KEY: Optional[str] = None
    RPC_URL: str = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY"
    OPENAI_API_KEY: Optional[str] = None

    # --- Embeddings / Vector Store ---
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    FAISS_INDEX_PATH: str = "./data/faiss.index"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"production", "staging", "development"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v = v.upper()
        if v not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
