"""Fresh live-job ingestion, normalization, and deduplication."""

import hashlib
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.job import Job, job_skills_table
from app.models.provider import Provider
from app.models.skill import Skill
from app.providers import build_provider_registry
from app.providers.base import JobProvider, NormalizedJob, ProviderQuery


@dataclass(slots=True)
class ProviderSyncResult:
    provider: str
    fetched: int = 0
    accepted: int = 0
    created: int = 0
    updated: int = 0
    rejected_stale: int = 0
    rejected_invalid: int = 0
    configured: bool = True
    error: str | None = None


class JobIngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_all(
        self,
        terms: list[str] | None = None,
        locations: list[str] | None = None,
        freshness_days: int | None = None,
    ) -> list[ProviderSyncResult]:
        days = max(1, min(freshness_days or settings.JOB_FRESHNESS_DAYS, 30))
        timeout = httpx.Timeout(30.0, connect=10.0)
        headers = {"User-Agent": "AIJobHunter/1.0 (+personal job search)"}
        results: list[ProviderSyncResult] = []
        async with httpx.AsyncClient(
            timeout=timeout, follow_redirects=True, headers=headers
        ) as client:
            for adapter in build_provider_registry(client):
                results.append(
                    await self._sync_provider(
                        adapter,
                        terms or [],
                        locations or [],
                        days,
                    )
                )
        await self._deactivate_stale(days)
        await self.db.commit()
        return results

    async def _sync_provider(
        self,
        adapter: JobProvider,
        terms: list[str],
        locations: list[str],
        freshness_days: int,
    ) -> ProviderSyncResult:
        provider = await self._provider_row(adapter)
        now = datetime.now(timezone.utc)
        provider.last_sync_at = now
        result = ProviderSyncResult(provider=adapter.slug, configured=adapter.configured)
        if not adapter.configured:
            provider.health_status = "not_configured"
            provider.last_error = "Provider credentials are not configured."
            return result

        try:
            pages = settings.JOB_SYNC_PAGES_PER_PROVIDER if adapter.paginated else 1
            normalized: list[NormalizedJob] = []
            for page in range(1, max(1, pages) + 1):
                normalized.extend(
                    await adapter.search_jobs(
                        ProviderQuery(
                            terms=terms,
                            locations=locations,
                            page=page,
                            freshness_days=freshness_days,
                        )
                    )
                )
            result.fetched = len(normalized)
            cutoff = now - timedelta(days=freshness_days)
            for item in normalized:
                if not self._valid(item):
                    result.rejected_invalid += 1
                    continue
                if item.posted_at < cutoff or item.posted_at > now + timedelta(hours=2):
                    result.rejected_stale += 1
                    continue
                created = await self._upsert_job(provider, item, now)
                result.accepted += 1
                if created:
                    result.created += 1
                else:
                    result.updated += 1
            provider.health_status = "healthy"
            provider.last_success_at = now
            provider.last_error = None
            provider.jobs_found = result.accepted
        except Exception as exc:
            result.error = str(exc)[:1000]
            provider.health_status = "error"
            provider.last_error = result.error
        return result

    async def _provider_row(self, adapter: JobProvider) -> Provider:
        result = await self.db.execute(select(Provider).where(Provider.slug == adapter.slug))
        provider = result.scalar_one_or_none()
        if provider is None:
            provider = Provider(
                name=adapter.name,
                slug=adapter.slug,
                base_url=adapter.base_url,
                is_builtin=True,
                is_active=True,
            )
            self.db.add(provider)
            await self.db.flush()
        return provider

    async def _upsert_job(self, provider: Provider, item: NormalizedJob, now: datetime) -> bool:
        fingerprint = self._fingerprint(item)
        result = await self.db.execute(
            select(Job).where(
                (Job.provider_id == str(provider.id)) & (Job.external_id == item.external_id)
            )
        )
        job = result.scalar_one_or_none()
        if job is None:
            result = await self.db.execute(select(Job).where(Job.fingerprint == fingerprint))
            job = result.scalar_one_or_none()

        created = job is None
        if job is None:
            job = Job(
                provider_id=str(provider.id),
                external_id=item.external_id,
                title=item.title,
                company=item.company,
                posted_at=item.posted_at,
                last_seen_at=now,
                fingerprint=fingerprint,
                url=item.url,
            )
            self.db.add(job)

        stored_posted_at = job.posted_at
        if stored_posted_at.tzinfo is None:
            stored_posted_at = stored_posted_at.replace(tzinfo=timezone.utc)
        if created or item.posted_at >= stored_posted_at:
            job.provider_id = str(provider.id)
            job.external_id = item.external_id
            job.title = item.title
            job.company = item.company
            job.location = item.location
            job.work_mode = item.work_mode
            job.salary_min = item.salary_min
            job.salary_max = item.salary_max
            job.salary_currency = item.salary_currency
            job.description = item.description
            job.url = item.url
            job.job_type = item.job_type
            job.posted_at = item.posted_at
            job.expires_at = item.expires_at
            job.source_metadata = item.metadata
        job.last_seen_at = now
        job.is_active = True
        job.is_duplicate = False
        await self.db.flush()
        await self._replace_skills(job, item.skills)
        return created

    async def _replace_skills(self, job: Job, names: list[str]) -> None:
        normalized = sorted({name.strip() for name in names if name.strip()})[:30]
        if not normalized:
            return
        for name in normalized:
            result = await self.db.execute(select(Skill).where(Skill.name == name))
            skill = result.scalar_one_or_none()
            if skill is None:
                skill = Skill(name=name)
                self.db.add(skill)
                await self.db.flush()
            exists = await self.db.execute(
                select(job_skills_table).where(
                    (job_skills_table.c.job_id == str(job.id))
                    & (job_skills_table.c.skill_id == str(skill.id))
                )
            )
            if exists.first() is None:
                await self.db.execute(
                    job_skills_table.insert().values(
                        job_id=str(job.id), skill_id=str(skill.id), is_required=True
                    )
                )

    async def _deactivate_stale(self, freshness_days: int) -> None:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=freshness_days)
        await self.db.execute(
            update(Job)
            .where(
                (Job.posted_at < cutoff) | ((Job.expires_at.is_not(None)) & (Job.expires_at < now))
            )
            .values(is_active=False)
        )

    @staticmethod
    def _valid(item: NormalizedJob) -> bool:
        return bool(
            item.external_id and item.title and item.company and item.url and item.posted_at
        )

    @staticmethod
    def _fingerprint(item: NormalizedJob) -> str:
        def normalize(value: str | None) -> str:
            return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()

        raw = "|".join((normalize(item.company), normalize(item.title), normalize(item.location)))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def sync_result_payload(result: ProviderSyncResult) -> dict[str, object]:
    return asdict(result)
