"""Job 和 JobSkill 模型。"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.provider import Provider
    from app.models.skill import Skill

# 多对多关联表：job <-> skills
job_skills_table = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", String(36), ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String(36), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
    Column("is_required", Boolean, default=True, nullable=False),
)


class Job(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "jobs"

    provider_id: Mapped[str] = mapped_column(String(36), ForeignKey("providers.id"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(500), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str | None] = mapped_column(String(500), nullable=True)
    work_mode: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # remote, hybrid, onsite
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    company_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    experience_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    job_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # full-time, part-time, contract
    posted_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # 关系
    provider: Mapped["Provider"] = relationship("Provider", back_populates="jobs")
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", secondary=job_skills_table, lazy="selectin"
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="job", lazy="selectin"
    )
