"""User settings schemas."""

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class SettingsUpdate(BaseModel):
    freshness_days: int | None = Field(default=None, ge=1, le=30)
    min_match_score: float | None = Field(default=None, ge=0, le=100)
    search_terms: list[str] | None = Field(default=None, max_length=20)
    locations: list[str] | None = Field(default=None, max_length=10)
    work_modes: list[str] | None = Field(default=None, max_length=3)
    email_enabled: bool | None = None
    telegram_enabled: bool | None = None
    slack_enabled: bool | None = None
    discord_enabled: bool | None = None
    telegram_chat_id: str | None = Field(default=None, max_length=255)
    slack_webhook_url: HttpUrl | None = None
    discord_webhook_url: HttpUrl | None = None


class SettingsRead(BaseModel):
    freshness_days: int
    min_match_score: float
    search_terms: list[str]
    locations: list[str]
    work_modes: list[str]
    email_enabled: bool
    telegram_enabled: bool
    slack_enabled: bool
    discord_enabled: bool
    telegram_chat_id: str | None
    slack_webhook_url: str | None
    discord_webhook_url: str | None
    last_notified_at: datetime | None

    model_config = {"from_attributes": True}
