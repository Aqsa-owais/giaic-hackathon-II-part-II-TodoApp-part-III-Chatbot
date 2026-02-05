from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    database_url: str = Field(default=...)

    # Authentication settings
    better_auth_secret: str = Field(default=...)
    frontend_url: str = Field(default="http://localhost:3000")

    # JWT settings
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # CORS settings - Allow multiple origins from environment variable
    allowed_origins_raw: str = Field(default="http://localhost:3000,http://localhost:3001")

    # OpenAI settings for AI Agent
    openai_api_key: str = Field(default=...)
    openai_model: str = Field(default="gpt-4o-mini")

    # MCP Tools settings
    mcp_tools_base_url: str = Field(default="http://localhost:8000")  # Default to local backend
    mcp_tools_timeout: int = Field(default=30)  # Timeout in seconds

    # Additional settings that may be in .env
    next_public_api_url: str = Field(default="http://localhost:8000")
    gemini_api_key: str = Field(default="")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra fields in .env that are not defined
    }

    def __init__(self, **data):
        super().__init__(**data)
        # Parse allowed_origins from the raw string
        self._allowed_origins = [origin.strip() for origin in self.allowed_origins_raw.split(",")]

    @property
    def allowed_origins(self) -> List[str]:
        return self._allowed_origins


def get_settings() -> Settings:
    """Get application settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


# Validate settings on startup
def validate_settings():
    """Validate that required settings are properly configured"""
    if not settings.database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    if not settings.better_auth_secret:
        raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

    if len(settings.better_auth_secret) < 32:
        raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters long")

    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")