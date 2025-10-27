"""
Application configuration and metadata utilities.
Avoid hardcoding config; read from environment where feasible.
"""

from functools import lru_cache
from typing import List
import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    app_name: str = Field(default=os.getenv("APP_NAME", "Notes API"))
    app_description: str = Field(
        default=os.getenv(
            "APP_DESCRIPTION",
            "A simple Notes management API with CRUD operations.",
        )
    )
    app_version: str = Field(default=os.getenv("APP_VERSION", "0.1.0"))
    allowed_origins: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
    )


@lru_cache
# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Get cached application settings populated from environment variables."""
    return Settings()
