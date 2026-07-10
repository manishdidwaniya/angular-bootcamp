"""API v1 主路由 — 聚合所有子路由。"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    analytics,
    applications,
    auth,
    jobs,
    notifications,
    profiles,
    providers,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
