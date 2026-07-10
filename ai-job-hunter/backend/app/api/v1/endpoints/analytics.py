"""User dashboard analytics."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.application import Application
from app.models.job import Job
from app.models.notification import Notification
from app.models.user import User

router = APIRouter()


@router.get("/summary")
async def analytics_summary(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    applications = await db.scalar(
        select(func.count()).select_from(Application).where(Application.user_id == str(user.id))
    )
    active_jobs = await db.scalar(
        select(func.count()).select_from(Job).where(Job.is_active.is_(True))
    )
    unread = await db.scalar(
        select(func.count())
        .select_from(Notification)
        .where(Notification.user_id == str(user.id), Notification.is_read.is_(False))
    )
    return {
        "applications": applications or 0,
        "active_jobs": active_jobs or 0,
        "unread_notifications": unread or 0,
    }
