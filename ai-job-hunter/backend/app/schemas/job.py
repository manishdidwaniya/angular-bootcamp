"""Job Pydantic schemas。"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class JobSkillRead(BaseModel):
    id: str
    name: str
    category: str | None

    model_config = {"from_attributes": True}


class JobRead(BaseModel):
    id: str
    provider_id: str
    external_id: str
    title: str
    company: str
    location: str | None
    work_mode: str | None
    salary_min: int | None
    salary_max: int | None
    salary_currency: str | None
    description: str | None
    url: str
    company_url: str | None
    experience_min: float | None
    experience_max: float | None
    job_type: str | None
    posted_at: str | None
    is_active: bool
    skills: list[JobSkillRead]
    created_at: datetime

    model_config = {"from_attributes": True}


class JobMatchResult(BaseModel):
    job: JobRead
    score: float = Field(ge=0, le=100)
    explanation: str
    strengths: list[str]
    missing_skills: list[str]
    recommendation: str  # strong_match, good_match, weak_match, skip
    suggested_resume_id: str | None = None


class JobSearchFilters(BaseModel):
    query: str | None = None
    location: str | None = None
    work_mode: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    job_type: str | None = None
    provider_ids: list[str] | None = None
    skills: list[str] | None = None
    posted_within_days: int | None = None
    min_score: float | None = Field(default=None, ge=0, le=100)


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
