"""Fresh job search and profile-aware recommendation endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.job import JobMatchResult, JobRead, JobSearchFilters, PaginatedResponse
from app.services.job_service import JobService

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def search_jobs(
    query: str | None = None,
    company: str | None = None,
    location: str | None = None,
    work_mode: str | None = None,
    posted_within_days: int = Query(7, ge=1, le=30),
    sort_by: str = Query("newest", pattern="^(newest|salary)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse:
    service = JobService(db)
    filters = JobSearchFilters(
        query=query,
        company=company,
        location=location,
        work_mode=work_mode,
        posted_within_days=posted_within_days,
        sort_by=sort_by,
    )
    return await service.search(filters, page, page_size)


@router.get("/recommended", response_model=PaginatedResponse)
async def recommended_jobs(
    query: str | None = None,
    location: str | None = None,
    work_mode: str | None = None,
    posted_within_days: int = Query(7, ge=1, le=30),
    min_score: float = Query(45, ge=0, le=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PaginatedResponse:
    service = JobService(db)
    filters = JobSearchFilters(
        query=query,
        location=location,
        work_mode=work_mode,
        posted_within_days=posted_within_days,
        min_score=min_score,
    )
    return await service.recommended(str(user.id), filters, page, page_size)


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)) -> JobRead:
    service = JobService(db)
    return service.to_read(await service.get_by_id(job_id))


@router.post("/{job_id}/match", response_model=JobMatchResult)
async def match_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JobMatchResult:
    service = JobService(db)
    return await service.match_job(job_id, str(user.id))
