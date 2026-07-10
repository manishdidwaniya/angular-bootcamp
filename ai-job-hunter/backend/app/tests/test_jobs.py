"""Job browsing and match-contract tests."""

from datetime import datetime, timezone

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
        description="Angular TypeScript role requiring 4 years of experience.",
        posted_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        fingerprint="a" * 64,
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

    registered = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "jobs@example.com",
            "password": "securepassword123",
            "full_name": "Job Seeker",
        },
    )
    headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}
    profile = await client.post(
        "/api/v1/profiles",
        headers=headers,
        json={
            "headline": "Angular Engineer",
            "experience_years": 5,
            "work_mode_preference": "remote",
            "skills": [{"name": "Angular", "proficiency_level": "advanced"}],
            "target_roles": [{"role_title": "Senior Angular Engineer"}],
        },
    )
    assert profile.status_code == 201, profile.text

    match = await client.post(f"/api/v1/jobs/{job.id}/match", headers=headers)
    assert match.status_code == 200
    assert match.json()["score"] >= 70
    assert match.json()["recommendation"] in {"good_match", "strong_match"}

    recommended = await client.get("/api/v1/jobs/recommended", headers=headers)
    assert recommended.status_code == 200, recommended.text
    assert recommended.json()["total"] == 1
    assert recommended.json()["items"][0]["job"]["source"] == "Example Jobs"

    tracked = await client.post(
        "/api/v1/applications", headers=headers, json={"job_id": str(job.id)}
    )
    assert tracked.status_code == 201, tracked.text
    applications = await client.get("/api/v1/applications", headers=headers)
    assert applications.status_code == 200
    assert applications.json()[0]["job"]["title"] == "Senior Angular Engineer"
