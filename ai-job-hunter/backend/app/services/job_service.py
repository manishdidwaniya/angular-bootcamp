"""Job 业务逻辑。"""

import math

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobMatchResult, JobRead, JobSearchFilters, PaginatedResponse


class JobService:
    """职位服务 — 搜索、获取、匹配。"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = JobRepository(db)

    async def search(
        self, filters: JobSearchFilters, page: int, page_size: int
    ) -> PaginatedResponse:
        """搜索职位，支持分页和过滤。"""
        query = select(Job).where(Job.is_active.is_(True), Job.is_duplicate.is_(False))

        if filters.query:
            query = query.where(Job.title.ilike(f"%{filters.query}%"))
        if filters.location:
            query = query.where(Job.location.ilike(f"%{filters.location}%"))
        if filters.work_mode:
            query = query.where(Job.work_mode == filters.work_mode)

        # 计数
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar() or 0

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Job.created_at.desc())
        result = await self.db.execute(query)
        jobs = result.scalars().all()

        return PaginatedResponse(
            items=[JobRead.model_validate(j) for j in jobs],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if total > 0 else 0,
        )

    async def get_by_id(self, job_id: str) -> Job:
        """根据 ID 获取职位。"""
        job = await self.repo.find_by_id(job_id)
        if not job:
            raise NotFoundException("Job", job_id)
        return job

    async def match_job(self, job_id: str) -> JobMatchResult:
        """对职位进行 AI 匹配评分（Phase 6 实现）。"""
        job = await self.get_by_id(job_id)
        # 占位 — Phase 6 将接入真实 AI 匹配
        return JobMatchResult(
            job=JobRead.model_validate(job),
            score=0.0,
            explanation="AI matching not yet implemented (Phase 6).",
            strengths=[],
            missing_skills=[],
            recommendation="skip",
            suggested_resume_id=None,
        )
