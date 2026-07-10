"""Arbeitnow provider backed by employer/ATS listings."""

from typing import Any

from app.providers.base import JobProvider, NormalizedJob, ProviderQuery
from app.providers.utils import clean_html, clean_list, utc_datetime


class ArbeitnowProvider(JobProvider):
    slug = "arbeitnow"
    name = "Arbeitnow"
    base_url = "https://www.arbeitnow.com/api/job-board-api"

    async def search_jobs(self, query: ProviderQuery) -> list[NormalizedJob]:
        response = await self.client.get(self.base_url, params={"page": query.page})
        response.raise_for_status()
        return [self.normalize(item) for item in response.json().get("data", [])]

    def normalize(self, raw: dict[str, Any]) -> NormalizedJob:
        remote = bool(raw.get("remote"))
        job_types = clean_list(raw.get("job_types"))
        return NormalizedJob(
            external_id=str(raw["slug"]),
            title=str(raw["title"]).strip(),
            company=str(raw["company_name"]).strip(),
            location=str(raw.get("location") or "Remote").strip(),
            work_mode="remote" if remote else "onsite",
            description=clean_html(str(raw.get("description") or "")),
            url=str(raw["url"]),
            posted_at=utc_datetime(raw["created_at"]),
            job_type=job_types[0] if job_types else None,
            skills=clean_list(raw.get("tags")),
            metadata={"remote": remote, "source": "Arbeitnow"},
        )
