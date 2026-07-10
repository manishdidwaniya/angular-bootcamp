"""Authentication 端点测试。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "email": "dup@example.com",
        "password": "securepassword123",
        "full_name": "Dup User",
    }
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient) -> None:
    # 先注册
    payload = {
        "email": "login@example.com",
        "password": "securepassword123",
        "full_name": "Login User",
    }
    await client.post("/api/v1/auth/register", json=payload)

    # 再登录
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_and_current_user(client: AsyncClient) -> None:
    payload = {
        "email": "refresh@example.com",
        "password": "securepassword123",
        "full_name": "Refresh User",
    }
    registered = (await client.post("/api/v1/auth/register", json=payload)).json()

    refreshed = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": registered["refresh_token"]},
    )
    assert refreshed.status_code == 200
    assert refreshed.json()["access_token"]

    current_user = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {registered['access_token']}"},
    )
    assert current_user.status_code == 200
    assert current_user.json()["email"] == payload["email"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
        "full_name": "Nobody",
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422
