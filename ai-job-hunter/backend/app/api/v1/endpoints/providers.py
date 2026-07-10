"""Live provider status and manual synchronization endpoints."""

import asyncio
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.profile import Profile
from app.models.provider import Provider
from app.models.user import User
from app.services.job_ingestion_service import JobIngestionService, sync_result_payload

router = APIRouter()
sync_lock = asyncio.Lock()


class SyncRequest(BaseModel):
    terms: list[str] = Field(default_factory=list, max_length=20)
    locations: list[str] = Field(default_factory=list, max_length=10)
    freshness_days: int = Field(default=7, ge=1, le=30)


@router.get("")
async def list_providers(db: AsyncSession = Depends(get_db)) -> list[dict[str, Any]]:
    result = await db.execute(select(Provider).order_by(Provider.name))
    return [
        {
            "id": str(provider.id),
            "name": provider.name,
            "slug": provider.slug,
            "base_url": provider.base_url,
            "is_active": provider.is_active,
            "health_status": provider.health_status,
            "last_sync_at": provider.last_sync_at,
            "last_success_at": provider.last_success_at,
            "last_error": provider.last_error,
            "jobs_found": provider.jobs_found,
        }
        for provider in result.scalars()
    ]


@router.post("/sync")
async def sync_providers(
    data: SyncRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, object]:
    if sync_lock.locked():
        return {"status": "already_running", "providers": []}
    terms = data.terms
    locations = data.locations
    if not terms or not locations:
        profile_result = await db.execute(select(Profile).where(Profile.user_id == str(user.id)))
        profile = profile_result.scalar_one_or_none()
        if profile is not None:
            terms = terms or [role.role_title for role in profile.target_roles if role.is_active]
            locations = locations or ([profile.location] if profile.location else [])
    async with sync_lock:
        results = await JobIngestionService(db).sync_all(terms, locations, data.freshness_days)
    return {
        "status": "completed",
        "providers": [sync_result_payload(result) for result in results],
        "created": sum(result.created for result in results),
        "accepted": sum(result.accepted for result in results),
    }
