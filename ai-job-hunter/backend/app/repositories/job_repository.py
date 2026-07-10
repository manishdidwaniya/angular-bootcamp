"""Job Repository。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):
    """职位数据访问层。"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Job)

    async def find_by_external_id(self, provider_id: str, external_id: str) -> Job | None:
        """根据外部 ID 查找职位（用于去重）。"""
        result = await self.db.execute(
            select(Job).where(
                Job.provider_id == provider_id,
                Job.external_id == external_id,
            )
        )
        return result.scalar_one_or_none()

    async def find_duplicates(self, title: str, company: str) -> list[Job]:
        """查找可能的重复职位。"""
        result = await self.db.execute(
            select(Job).where(
                Job.title.ilike(f"%{title}%"),
                Job.company.ilike(f"%{company}%"),
                Job.is_duplicate.is_(False),
            )
        )
        return list(result.scalars().all())
