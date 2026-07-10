"""Adzuna live search provider (enabled when API credentials are configured)."""

from typing import Any

from app.core.config import settings
from app.providers.base import JobProvider, NormalizedJob, ProviderQuery
from app.providers.utils import clean_html, utc_datetime


class AdzunaProvider(JobProvider):
    slug = "adzuna"
    name = "Adzuna"
    base_url = "https://api.adzuna.com/v1/api"
    requires_credentials = True

    @property
    def configured(self) -> bool:
        return bool(settings.ADZUNA_APP_ID and settings.ADZUNA_APP_KEY)

    async def search_jobs(self, query: ProviderQuery) -> list[NormalizedJob]:
        if not self.configured:
            return []
        endpoint = f"{self.base_url}/jobs/{settings.ADZUNA_COUNTRY}/search/{query.page}"
        params: dict[str, str | int] = {
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "results_per_page": 50,
            "sort_by": "date",
            "max_days_old": query.freshness_days,
            "content-type": "application/json",
        }
        if query.terms:
            params["what"] = " ".join(query.terms)
        if query.locations:
            params["where"] = " ".join(query.locations)
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return [self.normalize(item) for item in response.json().get("results", [])]

    def normalize(self, raw: dict[str, Any]) -> NormalizedJob:
        company = raw.get("company") or {}
        location = raw.get("location") or {}
        category = raw.get("category") or {}
        return NormalizedJob(
            external_id=str(raw["id"]),
            title=str(raw["title"]).strip(),
            company=str(company.get("display_name") or "Unknown company").strip(),
            location=str(location.get("display_name") or "").strip() or None,
            work_mode="remote" if "remote" in str(raw.get("description") or "").lower() else None,
            description=clean_html(str(raw.get("description") or "")),
            url=str(raw["redirect_url"]),
            posted_at=utc_datetime(raw["created"]),
            salary_min=int(raw["salary_min"]) if raw.get("salary_min") is not None else None,
            salary_max=int(raw["salary_max"]) if raw.get("salary_max") is not None else None,
            salary_currency="INR" if settings.ADZUNA_COUNTRY == "in" else None,
            job_type="contract" if raw.get("contract_time") else None,
            skills=[str(category.get("label"))] if category.get("label") else [],
            metadata={"source": "Adzuna"},
        )
