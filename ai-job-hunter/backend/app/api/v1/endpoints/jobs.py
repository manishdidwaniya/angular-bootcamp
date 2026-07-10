"""Jobs endpoints。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.job import Job
from app.schemas.job import JobMatchResult, JobRead, JobSearchFilters, PaginatedResponse
from app.services.job_service import JobService

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def search_jobs(
    query: str | None = None,
    location: str | None = None,
    work_mode: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse:
    """搜索职位，支持过滤和分页。"""
    service = JobService(db)
    filters = JobSearchFilters(
        query=query,
        location=location,
        work_mode=work_mode,
    )
    return await service.search(filters, page, page_size)


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)) -> Job:
    """获取单个职位详情。"""
    service = JobService(db)
    return await service.get_by_id(job_id)


@router.post("/{job_id}/match", response_model=JobMatchResult)
async def match_job(job_id: str, db: AsyncSession = Depends(get_db)) -> JobMatchResult:
    """对单个职位进行 AI 匹配评分。"""
    service = JobService(db)
    return await service.match_job(job_id)
