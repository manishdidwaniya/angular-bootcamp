"""Job browsing and match-contract tests."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job, job_skills_table
from app.models.provider import Provider
from app.models.skill import Skill


@pytest.mark.asyncio
async def test_job_search_detail_and_match(client: AsyncClient, db_session: AsyncSession) -> None:
    provider = Provider(name="Example Jobs", slug="example", base_url="https://example.com/jobs")
    skill = Skill(name="Angular", category="frontend")
    db_session.add_all([provider, skill])
    await db_session.flush()

    job = Job(
        provider_id=str(provider.id),
        external_id="example-1",
        title="Senior Angular Engineer",
        company="Example Ltd",
        location="Remote",
        work_mode="remote",
        url="https://example.com/jobs/1",
    )
    db_session.add(job)
    await db_session.flush()
    await db_session.execute(
        job_skills_table.insert().values(job_id=job.id, skill_id=skill.id, is_required=True)
    )
    await db_session.commit()

    search = await client.get("/api/v1/jobs", params={"query": "Angular"})
    assert search.status_code == 200, search.text
    assert search.json()["total"] == 1
    assert search.json()["items"][0]["skills"][0]["name"] == "Angular"

    detail = await client.get(f"/api/v1/jobs/{job.id}")
    assert detail.status_code == 200
    assert detail.json()["company"] == "Example Ltd"

    match = await client.post(f"/api/v1/jobs/{job.id}/match")
    assert match.status_code == 200
    assert match.json()["score"] == 0
