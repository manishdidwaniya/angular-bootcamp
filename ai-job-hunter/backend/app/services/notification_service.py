"""In-app and outbound notifications for fresh, high-match jobs."""

from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

import aiosmtplib
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.job import Job
from app.models.notification import Notification
from app.models.profile import Profile
from app.models.settings import UserSettings
from app.models.user import User
from app.services.job_service import JobService
from app.services.matching_service import MatchingService


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.matcher = MatchingService()

    async def notify_fresh_matches(self, lookback_minutes: int = 60) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=lookback_minutes)
        jobs_result = await self.db.execute(
            select(Job)
            .where(Job.is_active.is_(True), Job.created_at >= cutoff)
            .options(selectinload(Job.skills), selectinload(Job.provider))
        )
        jobs = jobs_result.scalars().unique().all()
        if not jobs:
            return 0

        profiles_result = await self.db.execute(
            select(Profile).options(
                selectinload(Profile.skills),
                selectinload(Profile.target_roles),
                selectinload(Profile.resumes),
                selectinload(Profile.user).selectinload(User.settings),
            )
        )
        sent = 0
        for profile in profiles_result.scalars().unique():
            preferences = profile.user.settings or UserSettings(user_id=str(profile.user.id))
            threshold = preferences.min_match_score
            for job in jobs:
                match = self.matcher.score(job, profile, JobService.to_read(job))
                if match.score < threshold:
                    continue
                created = await self._create_notification(
                    str(profile.user.id), str(job.id), "in_app", match
                )
                if not created:
                    continue
                sent += 1
                await self._dispatch_enabled(profile.user, preferences, job, match)
            preferences.last_notified_at = datetime.now(timezone.utc)
            if profile.user.settings is None:
                profile.user.settings = preferences
                self.db.add(preferences)
        await self.db.commit()
        return sent

    async def _create_notification(
        self, user_id: str, job_id: str, channel: str, match: object
    ) -> bool:
        result = await self.db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.job_id == job_id,
                Notification.channel == channel,
            )
        )
        if result.scalar_one_or_none() is not None:
            return False
        score = getattr(match, "score")
        job = getattr(match, "job")
        notification = Notification(
            user_id=user_id,
            job_id=job_id,
            channel=channel,
            title=f"{score:.0f}% match: {job.title}",
            message=f"{job.company} · {job.source} · posted {job.age_hours:.0f} hours ago",
            metadata_json=getattr(match, "model_dump_json")(),
        )
        self.db.add(notification)
        await self.db.flush()
        return True

    async def _dispatch_enabled(
        self, user: User, preferences: UserSettings, job: Job, match: object
    ) -> None:
        text = (
            f"{getattr(match, 'score'):.0f}% match — {job.title} at {job.company}\n"
            f"Posted: {job.posted_at.isoformat()}\n{job.url}"
        )
        if preferences.telegram_enabled:
            await self._telegram(preferences.telegram_chat_id, text)
        if preferences.slack_enabled:
            await self._webhook(preferences.slack_webhook_url or settings.SLACK_WEBHOOK_URL, text)
        if preferences.discord_enabled:
            await self._webhook(
                preferences.discord_webhook_url or settings.DISCORD_WEBHOOK_URL, text
            )
        if preferences.email_enabled:
            await self._email(user.email, f"Fresh job match: {job.title}", text)

    async def _telegram(self, chat_id: str | None, text: str) -> None:
        target = chat_id or settings.TELEGRAM_CHAT_ID
        if not settings.TELEGRAM_BOT_TOKEN or not target:
            return
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=15) as client:
            await client.post(url, json={"chat_id": target, "text": text})

    @staticmethod
    async def _webhook(url: str, text: str) -> None:
        if not url:
            return
        async with httpx.AsyncClient(timeout=15) as client:
            await client.post(url, json={"content": text, "text": text})

    @staticmethod
    async def _email(recipient: str, subject: str, text: str) -> None:
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD or not settings.SMTP_FROM_EMAIL:
            return
        message = EmailMessage()
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(text)
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
