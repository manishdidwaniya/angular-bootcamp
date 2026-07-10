"""APScheduler runtime for recurring search → normalize → deduplicate → match → notify."""

from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.database.session import async_session_factory
from app.models.profile import Profile
from app.services.job_ingestion_service import JobIngestionService
from app.services.notification_service import NotificationService


async def scheduled_job_pipeline() -> None:
    if not settings.ENABLE_LIVE_PROVIDERS:
        return
    async with async_session_factory() as db:
        result = await db.execute(select(Profile).options(selectinload(Profile.target_roles)))
        profiles = result.scalars().unique().all()
        terms = sorted(
            {
                role.role_title
                for profile in profiles
                for role in profile.target_roles
                if role.is_active
            }
        )[:20]
        locations = sorted({profile.location for profile in profiles if profile.location})[:10]
        await JobIngestionService(db).sync_all(terms, locations, settings.JOB_FRESHNESS_DAYS)
        await NotificationService(db).notify_fresh_matches(
            lookback_minutes=settings.JOB_SYNC_INTERVAL_MINUTES * 2
        )


def start_job_scheduler() -> AsyncIOScheduler | None:
    if not settings.SCHEDULER_ENABLED:
        return None
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        scheduled_job_pipeline,
        "interval",
        minutes=max(5, settings.JOB_SYNC_INTERVAL_MINUTES),
        id="live-job-pipeline",
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.now(timezone.utc) + timedelta(seconds=10),
    )
    scheduler.start()
    return scheduler
