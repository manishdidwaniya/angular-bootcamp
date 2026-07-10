"""We Work Remotely official RSS provider."""

import xml.etree.ElementTree as ET
from typing import Any

from app.providers.base import JobProvider, NormalizedJob, ProviderQuery
from app.providers.utils import clean_html, utc_datetime


class WeWorkRemotelyProvider(JobProvider):
    slug = "weworkremotely"
    name = "We Work Remotely"
    base_url = "https://weworkremotely.com/remote-jobs.rss"
    paginated = False

    async def search_jobs(self, query: ProviderQuery) -> list[NormalizedJob]:
        response = await self.client.get(self.base_url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        jobs: list[NormalizedJob] = []
        for item in root.findall("./channel/item"):
            raw = {child.tag.split("}")[-1]: child.text for child in item}
            jobs.append(self.normalize(raw))
        return jobs

    def normalize(self, raw: dict[str, Any]) -> NormalizedJob:
        combined_title = str(raw.get("title") or "").strip()
        company, separator, title = combined_title.partition(":")
        if not separator:
            company, title = "Unknown company", combined_title
        skills = [part.strip() for part in str(raw.get("skills") or "").split(",") if part.strip()]
        location = str(raw.get("region") or raw.get("country") or "Remote").strip()
        return NormalizedJob(
            external_id=str(raw.get("guid") or raw.get("link")),
            title=title.strip(),
            company=company.strip(),
            location=location,
            work_mode="remote",
            description=clean_html(str(raw.get("description") or "")),
            url=str(raw.get("link") or raw.get("guid")),
            posted_at=utc_datetime(raw["pubDate"]),
            expires_at=utc_datetime(raw["expires_at"]) if raw.get("expires_at") else None,
            job_type=str(raw.get("type") or "") or None,
            skills=skills,
            metadata={"category": raw.get("category"), "source": "We Work Remotely"},
        )
