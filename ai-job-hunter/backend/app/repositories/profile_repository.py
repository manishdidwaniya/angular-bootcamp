"""Profile Repository。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.repositories.base_repository import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    """档案数据访问层。"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Profile)

    async def find_by_user_id(self, user_id: str) -> Profile | None:
        """根据用户 ID 查找档案。"""
        result = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalar_one_or_none()
