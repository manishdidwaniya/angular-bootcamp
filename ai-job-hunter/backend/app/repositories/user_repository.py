"""User Repository。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问层。"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def find_by_email(self, email: str) -> User | None:
        """根据邮箱查找用户。"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def find_by_oauth(self, provider: str, provider_id: str) -> User | None:
        """根据 OAuth 信息查找用户。"""
        result = await self.db.execute(
            select(User).where(
                User.oauth_provider == provider,
                User.oauth_provider_id == provider_id,
            )
        )
        return result.scalar_one_or_none()
