"""Authenticated profile and dashboard API tests."""

import pytest
from httpx import AsyncClient


async def authenticated_headers(client: AsyncClient) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "profile@example.com",
            "password": "securepassword123",
            "full_name": "Profile User",
        },
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.mark.asyncio
async def test_profile_lifecycle(client: AsyncClient) -> None:
    headers = await authenticated_headers(client)
    created = await client.post(
        "/api/v1/profiles",
        headers=headers,
        json={
            "headline": "Angular and Python Engineer",
            "location": "Remote",
            "preferred_companies": ["OpenAI"],
            "skills": [
                {"name": "Angular", "proficiency_level": "advanced", "years_of_experience": 5}
            ],
            "target_roles": [{"role_title": "Senior Full-stack Engineer", "priority": 1}],
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["headline"] == "Angular and Python Engineer"

    profile = await client.get("/api/v1/profiles/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["preferred_companies"] == ["OpenAI"]


@pytest.mark.asyncio
async def test_dashboard_summary_requires_authentication(client: AsyncClient) -> None:
    anonymous = await client.get("/api/v1/analytics/summary")
    assert anonymous.status_code == 401

    headers = await authenticated_headers(client)
    summary = await client.get("/api/v1/analytics/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json() == {
        "applications": 0,
        "active_jobs": 0,
        "unread_notifications": 0,
    }
