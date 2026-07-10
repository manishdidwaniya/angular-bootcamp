"""Profiles endpoints。"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from app.services.profile_service import ProfileService

router = APIRouter()


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    data: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Profile:
    """创建用户档案。"""
    service = ProfileService(db)
    return await service.create(str(user.id), data)


@router.get("/me", response_model=ProfileRead)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Profile:
    """获取当前用户的档案。"""
    service = ProfileService(db)
    return await service.get_by_user_id(str(user.id))


@router.put("/me", response_model=ProfileRead)
async def update_my_profile(
    data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Profile:
    """更新当前用户的档案。"""
    service = ProfileService(db)
    return await service.update(str(user.id), data)
