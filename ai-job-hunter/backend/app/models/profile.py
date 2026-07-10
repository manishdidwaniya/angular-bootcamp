"""Profile, ProfileSkill, TargetRole 模型。"""

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.skill import Skill
    from app.models.user import User

# 多对多关联表：profile <-> skills
profile_skills_table = Table(
    "profile_skills",
    Base.metadata,
    Column(
        "profile_id", String(36), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("skill_id", String(36), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
    Column("proficiency_level", String(50), nullable=False, default="intermediate"),
    Column("years_of_experience", Float, nullable=False, default=0.0),
)


class Profile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_mode_preference: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # remote, hybrid, onsite
    min_salary: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_salary: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    experience_years: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    notice_period_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_companies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    ignored_companies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    certifications: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    languages: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="profile")
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", secondary=profile_skills_table, lazy="selectin"
    )
    target_roles: Mapped[list["TargetRole"]] = relationship(
        "TargetRole", back_populates="profile", lazy="selectin", cascade="all, delete-orphan"
    )
    resumes: Mapped[list["Resume"]] = relationship(
        "Resume", back_populates="profile", lazy="selectin", cascade="all, delete-orphan"
    )


class TargetRole(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "target_roles"

    profile_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # 关系
    profile: Mapped["Profile"] = relationship("Profile", back_populates="target_roles")
