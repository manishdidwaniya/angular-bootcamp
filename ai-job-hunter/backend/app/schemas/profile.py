"""Profile Pydantic schemas。"""

from datetime import datetime

from pydantic import BaseModel, Field


class SkillInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    proficiency_level: str = Field(
        default="intermediate"
    )  # beginner, intermediate, advanced, expert
    years_of_experience: float = Field(default=0.0, ge=0)


class TargetRoleInput(BaseModel):
    role_title: str = Field(min_length=1, max_length=255)
    priority: int = Field(default=1, ge=1, le=10)
    is_active: bool = True


class ProfileCreate(BaseModel):
    headline: str | None = Field(default=None, max_length=500)
    summary: str | None = None
    location: str | None = Field(default=None, max_length=255)
    work_mode_preference: str | None = None
    min_salary: int | None = Field(default=None, ge=0)
    max_salary: int | None = Field(default=None, ge=0)
    salary_currency: str = "USD"
    experience_years: float = Field(default=0.0, ge=0)
    notice_period_days: int | None = Field(default=None, ge=0)
    preferred_companies: list[str] = Field(default_factory=list)
    ignored_companies: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    skills: list[SkillInput] = Field(default_factory=list)
    target_roles: list[TargetRoleInput] = Field(default_factory=list)


class ProfileUpdate(BaseModel):
    headline: str | None = None
    summary: str | None = None
    location: str | None = None
    work_mode_preference: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    salary_currency: str | None = None
    experience_years: float | None = None
    notice_period_days: int | None = None
    preferred_companies: list[str] | None = None
    ignored_companies: list[str] | None = None
    certifications: list[str] | None = None
    languages: list[str] | None = None
    skills: list[SkillInput] | None = None
    target_roles: list[TargetRoleInput] | None = None


class SkillRead(BaseModel):
    id: str
    name: str
    category: str | None

    model_config = {"from_attributes": True}


class TargetRoleRead(BaseModel):
    id: str
    role_title: str
    priority: int
    is_active: bool

    model_config = {"from_attributes": True}


class ProfileRead(BaseModel):
    id: str
    headline: str | None
    summary: str | None
    location: str | None
    work_mode_preference: str | None
    min_salary: int | None
    max_salary: int | None
    salary_currency: str
    experience_years: float
    notice_period_days: int | None
    preferred_companies: list[str]
    ignored_companies: list[str]
    certifications: list[str]
    languages: list[str]
    skills: list[SkillRead]
    target_roles: list[TargetRoleRead]
    created_at: datetime

    model_config = {"from_attributes": True}
