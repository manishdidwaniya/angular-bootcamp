"""AI Job Hunter Platform — FastAPI Application Entry Point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.database.base import Base
from app.database.session import engine
from app.scheduler import start_job_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """应用生命周期：启动和关闭时执行。"""
    # 启动
    print(f"AI Job Hunter starting in {settings.ENVIRONMENT} mode...")
    if not settings.is_production:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    scheduler = start_job_scheduler()
    yield
    # 关闭
    if scheduler is not None:
        scheduler.shutdown(wait=False)
    await engine.dispose()
    print("AI Job Hunter shut down.")


def create_app() -> FastAPI:
    """工厂函数创建 FastAPI 实例。"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered job hunting platform API",
        version="0.1.0",
        docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 路由
    app.include_router(api_router, prefix="/api/v1")

    # 异常处理
    register_exception_handlers(app)

    # 健康检查
    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()
