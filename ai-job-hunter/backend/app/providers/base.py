"""Provider contract and normalized job representation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass(slots=True)
class ProviderQuery:
    terms: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    page: int = 1
    freshness_days: int = 7


@dataclass(slots=True)
class NormalizedJob:
    external_id: str
    title: str
    company: str
    location: str | None
    work_mode: str | None
    description: str
    url: str
    posted_at: datetime
    expires_at: datetime | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    job_type: str | None = None
    skills: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class JobProvider(ABC):
    slug: str
    name: str
    base_url: str
    requires_credentials: bool = False
    paginated: bool = True

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @property
    def configured(self) -> bool:
        return True

    @abstractmethod
    async def search_jobs(self, query: ProviderQuery) -> list[NormalizedJob]:
        """Fetch and normalize one page of jobs."""

    @abstractmethod
    def normalize(self, raw: dict[str, Any]) -> NormalizedJob:
        """Convert provider-specific data into the canonical shape."""

    async def health_check(self) -> tuple[bool, str | None]:
        try:
            response = await self.client.get(self.base_url)
            response.raise_for_status()
            return True, None
        except Exception as exc:
            return False, str(exc)
