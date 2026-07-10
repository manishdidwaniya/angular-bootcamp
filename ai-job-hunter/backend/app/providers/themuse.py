"""The Muse public jobs API provider."""

from typing import Any

from app.core.config import settings
from app.providers.base import JobProvider, NormalizedJob, ProviderQuery
from app.providers.utils import clean_html, clean_list, utc_datetime


class TheMuseProvider(JobProvider):
    slug = "themuse"
    name = "The Muse"
    base_url = "https://www.themuse.com/api/public/jobs"

    async def search_jobs(self, query: ProviderQuery) -> list[NormalizedJob]:
        params: dict[str, str | int] = {"page": query.page, "descending": "true"}
        if settings.THEMUSE_API_KEY:
            params["api_key"] = settings.THEMUSE_API_KEY
        response = await self.client.get(self.base_url, params=params)
        response.raise_for_status()
        return [self.normalize(item) for item in response.json().get("results", [])]

    def normalize(self, raw: dict[str, Any]) -> NormalizedJob:
        locations = raw.get("locations") or []
        location_names = [str(item.get("name")) for item in locations if item.get("name")]
        categories = [str(item.get("name")) for item in raw.get("categories") or []]
        levels = [str(item.get("name")) for item in raw.get("levels") or []]
        refs = raw.get("refs") or {}
        company = raw.get("company") or {}
        return NormalizedJob(
            external_id=str(raw["id"]),
            title=str(raw["name"]).strip(),
            company=str(company.get("name") or "Unknown company").strip(),
            location=", ".join(location_names) or None,
            work_mode=(
                "remote" if any("remote" in item.lower() for item in location_names) else None
            ),
            description=clean_html(str(raw.get("contents") or "")),
            url=str(refs.get("landing_page") or ""),
            posted_at=utc_datetime(raw["publication_date"]),
            job_type=str(raw.get("type") or "") or None,
            skills=clean_list(categories + levels + list(raw.get("tags") or [])),
            metadata={"source": "The Muse"},
        )
