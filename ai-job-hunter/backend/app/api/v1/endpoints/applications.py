"""Job-application tracking endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, get_db
from app.core.exceptions import NotFoundException
from app.models.application import Application
from app.models.job import Job
from app.models.user import User

router = APIRouter()


class ApplicationCreate(BaseModel):
    job_id: str
    resume_id: str | None = None
    notes: str | None = Field(default=None, max_length=5000)


class ApplicationUpdate(BaseModel):
    status: str | None = Field(
        default=None, pattern="^(applied|interviewing|offered|rejected|withdrawn)$"
    )
    notes: str | None = Field(default=None, max_length=5000)


def application_payload(application: Application) -> dict[str, Any]:
    return {
        "id": str(application.id),
        "job_id": str(application.job_id),
        "resume_id": str(application.resume_id) if application.resume_id else None,
        "status": application.status,
        "notes": application.notes,
        "ai_match_score": application.ai_match_score,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
        "job": {
            "title": application.job.title,
            "company": application.job.company,
            "url": application.job.url,
        },
    }


@router.get("")
async def list_applications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job))
        .where(Application.user_id == str(user.id))
        .order_by(Application.created_at.desc())
    )
    return [application_payload(item) for item in result.scalars()]


@router.post("", status_code=201)
async def create_application(
    data: ApplicationCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if await db.get(Job, data.job_id) is None:
        raise NotFoundException("Job", data.job_id)
    application = Application(user_id=str(user.id), **data.model_dump())
    db.add(application)
    await db.flush()
    await db.refresh(application, attribute_names=["job"])
    return application_payload(application)


@router.patch("/{application_id}")
async def update_application(
    application_id: str,
    data: ApplicationUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job))
        .where(
            Application.id == application_id,
            Application.user_id == str(user.id),
        )
    )
    application = result.scalar_one_or_none()
    if application is None:
        raise NotFoundException("Application", application_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(application, key, value)
    await db.flush()
    await db.refresh(application)
    return application_payload(application)
