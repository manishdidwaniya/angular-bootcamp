"""Job-provider endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.provider import Provider

router = APIRouter()


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
        }
        for provider in result.scalars()
    ]
