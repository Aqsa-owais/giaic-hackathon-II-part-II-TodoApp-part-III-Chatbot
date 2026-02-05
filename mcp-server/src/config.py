"""Configuration management for MCP Server."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database configuration - optional for testing
    database_url: Optional[str] = Field(default=None)
    
    # MCP Server configuration
    mcp_server_name: str = "task-management-server"
    mcp_server_version: str = "1.0.0"
    
    # Development configuration
    debug: bool = False
    log_level: str = "INFO"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


def get_settings() -> Settings:
    """Get application settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


def validate_settings():
    """Validate that required settings are properly configured"""
    if not settings.database_url:
        raise ValueError("DATABASE_URL environment variable is not set")