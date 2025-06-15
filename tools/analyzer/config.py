"""Configuration module for LLM providers."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class LLMConfig(BaseSettings):
    """Configuration for LLM providers."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: LLMProvider = Field(
        default=LLMProvider.GOOGLE,
        description="LLM provider to use",
    )

    # API Keys
    google_api_key: str | None = Field(
        default=None,
        alias="GOOGLE_API_KEY",
        description="Google API key for Gemini",
    )
    anthropic_api_key: str | None = Field(
        default=None,
        alias="ANTHROPIC_API_KEY",
        description="Anthropic API key for Claude",
    )
    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="OpenAI API key",
    )

    # Model names
    google_model: str = Field(
        default="gemini-2.5-pro-preview-06-05",
        description="Google model name",
    )
    anthropic_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Anthropic model name",
    )
    openai_model: str = Field(
        default="o4-mini-2025-04-16",
        description="OpenAI model name",
    )

    # Model parameters
    temperature: float | None = Field(
        default=None,
        ge=0,
        le=2,
        description="Temperature for generation",
    )
    max_tokens: int = Field(
        default=1024 * 32,
        gt=0,
        description="Maximum tokens for generation",
    )

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate provider value."""
        try:
            return LLMProvider(v.lower())
        except ValueError:
            raise ValueError(  # noqa: B904
                f"Invalid provider: {v}. Must be one of: {', '.join([p.value for p in LLMProvider])}"
            )

    def get_api_key(self) -> str:
        """Get API key for the configured provider."""
        if self.provider == LLMProvider.GOOGLE:
            if not self.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required for Google provider")
            return self.google_api_key
        elif self.provider == LLMProvider.ANTHROPIC:
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")
            return self.anthropic_api_key
        elif self.provider == LLMProvider.OPENAI:
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            return self.openai_api_key
        raise ValueError(f"Unknown provider: {self.provider}")

    def get_model_name(self) -> str:
        """Get model name for the configured provider."""
        if self.provider == LLMProvider.GOOGLE:
            return self.google_model
        elif self.provider == LLMProvider.ANTHROPIC:
            return self.anthropic_model
        elif self.provider == LLMProvider.OPENAI:
            return self.openai_model
        raise ValueError(f"Unknown provider: {self.provider}")

    def get_model_config(self) -> dict[str, Any]:
        """Get model configuration parameters."""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
