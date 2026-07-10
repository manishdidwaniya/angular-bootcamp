"""Search 模型 — 记录搜索历史。"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Search(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "searches"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    query: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    provider_ids: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array
    results_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    filters_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="searches")
