"""Resume schemas for matching against job descriptions."""

from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    parsed_content: str = Field(min_length=50, max_length=100_000)
    is_primary: bool = False


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    parsed_content: str | None = Field(default=None, min_length=50, max_length=100_000)
    is_primary: bool | None = None
    is_active: bool | None = None


class ResumeRead(BaseModel):
    id: str
    title: str
    parsed_content: str | None
    is_primary: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
