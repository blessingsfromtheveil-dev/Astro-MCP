"""
Application configuration for Astro-MCP.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "Astro-MCP"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------

    host: str = "127.0.0.1"
    port: int = 8000

    reload: bool = False

    # ------------------------------------------------------------------
    # Swiss Ephemeris
    # ------------------------------------------------------------------

    ephemeris_path: Path = Field(
        default=Path("./ephe"),
        description="Swiss Ephemeris data directory.",
    )

    # ------------------------------------------------------------------
    # Astrology Defaults
    # ------------------------------------------------------------------

    zodiac: str = "tropical"

    house_system: str = "W"

    sidereal_mode: str = "lahiri"

    topocentric: bool = True

    altitude: float = 0.0

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = "INFO"

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    cors_origins: list[str] = [
        "*",
    ]

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    api_prefix: str = "/api"

    enable_docs: bool = True

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    max_year: int = 3000

    min_year: int = 1800


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
