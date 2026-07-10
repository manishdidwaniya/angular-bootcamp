"""In-app notification endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.core.exceptions import NotFoundException
from app.models.notification import Notification
from app.models.user import User

router = APIRouter()


def notification_payload(notification: Notification) -> dict[str, Any]:
    return {
        "id": str(notification.id),
        "channel": notification.channel,
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "is_sent": notification.is_sent,
        "created_at": notification.created_at,
    }


@router.get("")
async def list_notifications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == str(user.id))
        .order_by(Notification.created_at.desc())
    )
    return [notification_payload(item) for item in result.scalars()]


@router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == str(user.id),
        )
    )
    notification = result.scalar_one_or_none()
    if notification is None:
        raise NotFoundException("Notification", notification_id)
    notification.is_read = True
    await db.flush()
    return notification_payload(notification)
