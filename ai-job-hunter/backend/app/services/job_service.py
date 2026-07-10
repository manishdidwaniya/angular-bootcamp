"""Latest-job search, pagination, and profile-aware recommendations."""

import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import NotFoundException, ValidationException
from app.models.job import Job
from app.models.skill import Skill
from app.repositories.job_repository import JobRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.job import (
    JobMatchResult,
    JobRead,
    JobSearchFilters,
    JobSkillRead,
    PaginatedResponse,
)
from app.services.matching_service import MatchingService


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = JobRepository(db)
        self.profile_repo = ProfileRepository(db)
        self.matcher = MatchingService()

    async def search(
        self, filters: JobSearchFilters, page: int, page_size: int
    ) -> PaginatedResponse:
        days = filters.posted_within_days or settings.JOB_FRESHNESS_DAYS
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = select(Job).where(
            Job.is_active.is_(True),
            Job.is_duplicate.is_(False),
            Job.posted_at >= cutoff,
        )

        if filters.query:
            pattern = f"%{filters.query.strip()}%"
            query = query.where(
                or_(
                    Job.title.ilike(pattern),
                    Job.company.ilike(pattern),
                    Job.description.ilike(pattern),
                )
            )
        if filters.location:
            query = query.where(Job.location.ilike(f"%{filters.location.strip()}%"))
        if filters.company:
            query = query.where(Job.company.ilike(f"%{filters.company.strip()}%"))
        if filters.work_mode:
            query = query.where(Job.work_mode == filters.work_mode)
        if filters.salary_min is not None:
            query = query.where(Job.salary_max >= filters.salary_min)
        if filters.salary_max is not None:
            query = query.where(Job.salary_min <= filters.salary_max)
        if filters.job_type:
            query = query.where(Job.job_type == filters.job_type)
        if filters.provider_ids:
            query = query.where(Job.provider_id.in_(filters.provider_ids))
        if filters.skills:
            for skill_name in filters.skills:
                query = query.where(Job.skills.any(Skill.name.ilike(f"%{skill_name}%")))

        count_query = select(func.count()).select_from(query.order_by(None).subquery())
        total = (await self.db.execute(count_query)).scalar() or 0

        order = (
            Job.salary_max.desc().nullslast()
            if filters.sort_by == "salary"
            else Job.posted_at.desc()
        )
        offset = (page - 1) * page_size
        result = await self.db.execute(query.order_by(order).offset(offset).limit(page_size))
        jobs = result.scalars().unique().all()

        return PaginatedResponse(
            items=[self.to_read(job) for job in jobs],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if total > 0 else 0,
        )

    async def recommended(
        self,
        user_id: str,
        filters: JobSearchFilters,
        page: int,
        page_size: int,
    ) -> PaginatedResponse:
        profile = await self.profile_repo.find_by_user_id(user_id)
        if profile is None:
            raise ValidationException(
                "Create your career profile before requesting recommendations."
            )
        days = filters.posted_within_days or settings.JOB_FRESHNESS_DAYS
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = select(Job).where(
            Job.is_active.is_(True), Job.is_duplicate.is_(False), Job.posted_at >= cutoff
        )
        if filters.query:
            pattern = f"%{filters.query.strip()}%"
            query = query.where(
                or_(
                    Job.title.ilike(pattern),
                    Job.company.ilike(pattern),
                    Job.description.ilike(pattern),
                )
            )
        if filters.location:
            location_pattern = f"%{filters.location.strip()}%"
            query = query.where(
                or_(Job.location.ilike(location_pattern), Job.work_mode == "remote")
            )
        if filters.company:
            query = query.where(Job.company.ilike(f"%{filters.company.strip()}%"))
        if filters.work_mode:
            query = query.where(Job.work_mode == filters.work_mode)
        if filters.skills:
            for skill_name in filters.skills:
                query = query.where(Job.skills.any(Skill.name.ilike(f"%{skill_name}%")))
        result = await self.db.execute(query.order_by(Job.posted_at.desc()).limit(500))
        matches = [
            self.matcher.score(job, profile, self.to_read(job)) for job in result.scalars().unique()
        ]
        minimum_score = filters.min_score if filters.min_score is not None else 45.0
        matches = [match for match in matches if match.score >= minimum_score]
        matches.sort(key=lambda match: (match.score, match.job.posted_at), reverse=True)
        total = len(matches)
        start = (page - 1) * page_size
        return PaginatedResponse(
            items=matches[start : start + page_size],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )

    async def get_by_id(self, job_id: str) -> Job:
        job = await self.repo.find_by_id(job_id)
        if not job:
            raise NotFoundException("Job", job_id)
        return job

    async def match_job(self, job_id: str, user_id: str) -> JobMatchResult:
        job = await self.get_by_id(job_id)
        profile = await self.profile_repo.find_by_user_id(user_id)
        if profile is None:
            raise ValidationException("Create your career profile before matching jobs.")
        return self.matcher.score(job, profile, self.to_read(job))

    @staticmethod
    def to_read(job: Job) -> JobRead:
        posted_at = job.posted_at
        if posted_at.tzinfo is None:
            posted_at = posted_at.replace(tzinfo=timezone.utc)
        age_hours = max(0.0, (datetime.now(timezone.utc) - posted_at).total_seconds() / 3600)
        return JobRead(
            id=str(job.id),
            provider_id=str(job.provider_id),
            external_id=job.external_id,
            title=job.title,
            company=job.company,
            location=job.location,
            work_mode=job.work_mode,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            salary_currency=job.salary_currency,
            description=job.description,
            url=job.url,
            company_url=job.company_url,
            experience_min=job.experience_min,
            experience_max=job.experience_max,
            job_type=job.job_type,
            posted_at=posted_at,
            expires_at=job.expires_at,
            source=job.provider.name,
            age_hours=round(age_hours, 1),
            is_active=job.is_active,
            skills=[JobSkillRead.model_validate(skill) for skill in job.skills],
            created_at=job.created_at,
        )
