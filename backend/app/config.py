"""Minimal settings loader for BAHR MVP.

Reads environment variables with sensible defaults for the currently
implemented subset. Expands easily later without breaking imports.

Referenced in: ARCHITECTURE_OVERVIEW.md (Environment Catalog)
"""
from __future__ import annotations

from dataclasses import dataclass
import os


def _get(name: str, default: str | None = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val if val is not None else ""


@dataclass(slots=True)
class Settings:
    project_name: str = _get("PROJECT_NAME", "BAHR API")
    version: str = _get("API_VERSION", "1.0.0")
    analysis_engine_version: str = _get("ANALYSIS_ENGINE_VERSION", "1.0.0")
    log_level: str = _get("LOG_LEVEL", "INFO")
    secret_key: str = _get("SECRET_KEY", "dev-insecure-key", required=False)
    
    # CORS configuration (ADR-003: Explicit CORS origins)
    cors_origins: list[str] = None
    
    def __post_init__(self):
        """Initialize CORS origins from environment or defaults."""
        if self.cors_origins is None:
            cors_str = _get("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
            self.cors_origins = [origin.strip() for origin in cors_str.split(",")]
    
    # Future (placeholders, not yet wired in code):
    database_url: str = _get("DATABASE_URL", "")
    redis_url: str = _get("REDIS_URL", "")
    rate_limit_requests: int = int(_get("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_period: int = int(_get("RATE_LIMIT_PERIOD", "3600"))
    maintenance_mode: bool = _get("MAINTENANCE_MODE", "false").lower() == "true"


settings = Settings()

__all__ = ["settings", "Settings"]
