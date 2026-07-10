"""Search and notification preference endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.settings import UserSettings
from app.models.user import User
from app.schemas.settings import SettingsRead, SettingsUpdate

router = APIRouter()


async def get_or_create_settings(db: AsyncSession, user_id: str) -> UserSettings:
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    preferences = result.scalar_one_or_none()
    if preferences is None:
        preferences = UserSettings(user_id=user_id)
        db.add(preferences)
        await db.flush()
        await db.refresh(preferences)
    return preferences


@router.get("/me", response_model=SettingsRead)
async def get_settings(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserSettings:
    return await get_or_create_settings(db, str(user.id))


@router.put("/me", response_model=SettingsRead)
async def update_settings(
    data: SettingsUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserSettings:
    preferences = await get_or_create_settings(db, str(user.id))
    for key, value in data.model_dump(exclude_unset=True).items():
        if key.endswith("_webhook_url") and value is not None:
            value = str(value)
        setattr(preferences, key, value)
    await db.flush()
    await db.refresh(preferences)
    return preferences
