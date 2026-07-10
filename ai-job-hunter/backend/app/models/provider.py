"""Provider 模型 — 可插拔的职位数据源。"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.job import Job


class Provider(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "providers"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    config: Mapped[str | None] = mapped_column(String(2000), nullable=True)  # JSON: api_key, etc.
    last_health_check: Mapped[str | None] = mapped_column(String(50), nullable=True)
    health_status: Mapped[str] = mapped_column(String(20), default="unknown", nullable=False)
    rate_limit_per_minute: Mapped[int] = mapped_column(default=30, nullable=False)

    # 关系
    jobs: Mapped[list["Job"]] = relationship("Job", back_populates="provider", lazy="selectin")
