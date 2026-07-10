"""Multiple-resume management endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.core.exceptions import NotFoundException, ValidationException
from app.models.profile import Profile
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeRead, ResumeUpdate

router = APIRouter()


async def profile_id_for(db: AsyncSession, user_id: str) -> str:
    result = await db.execute(select(Profile.id).where(Profile.user_id == user_id))
    profile_id = result.scalar_one_or_none()
    if profile_id is None:
        raise ValidationException("Create your career profile before adding resumes.")
    return str(profile_id)


@router.get("", response_model=list[ResumeRead])
async def list_resumes(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Resume]:
    profile_id = await profile_id_for(db, str(user.id))
    result = await db.execute(
        select(Resume).where(Resume.profile_id == profile_id).order_by(Resume.created_at.desc())
    )
    return list(result.scalars())


@router.post("", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
async def create_resume(
    data: ResumeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Resume:
    profile_id = await profile_id_for(db, str(user.id))
    if data.is_primary:
        await db.execute(
            update(Resume).where(Resume.profile_id == profile_id).values(is_primary=False)
        )
    resume = Resume(
        profile_id=profile_id,
        title=data.title,
        parsed_content=data.parsed_content,
        file_type="text",
        is_primary=data.is_primary,
    )
    db.add(resume)
    await db.flush()
    await db.refresh(resume)
    return resume


@router.put("/{resume_id}", response_model=ResumeRead)
async def update_resume(
    resume_id: str,
    data: ResumeUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Resume:
    profile_id = await profile_id_for(db, str(user.id))
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.profile_id == profile_id)
    )
    resume = result.scalar_one_or_none()
    if resume is None:
        raise NotFoundException("Resume", resume_id)
    values = data.model_dump(exclude_unset=True)
    if values.get("is_primary"):
        await db.execute(
            update(Resume).where(Resume.profile_id == profile_id).values(is_primary=False)
        )
    for key, value in values.items():
        setattr(resume, key, value)
    await db.flush()
    await db.refresh(resume)
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    profile_id = await profile_id_for(db, str(user.id))
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.profile_id == profile_id)
    )
    resume = result.scalar_one_or_none()
    if resume is None:
        raise NotFoundException("Resume", resume_id)
    await db.delete(resume)
