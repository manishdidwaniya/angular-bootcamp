"""Application 模型 — 跟踪求职申请。"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.user import User


class Application(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "applications"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    resume_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("resumes.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="applied", nullable=False
    )  # applied, interviewing, offered, rejected, withdrawn
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_match_score: Mapped[float | None] = mapped_column(nullable=True)
    ai_match_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_updated_at: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")
