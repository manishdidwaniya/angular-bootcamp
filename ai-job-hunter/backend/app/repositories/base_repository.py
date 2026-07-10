"""基础 Repository — 提供通用 CRUD 操作。"""

from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """所有 Repository 的基类，封装通用数据访问逻辑。"""

    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def find_by_id(self, id: str) -> ModelType | None:
        """根据主键查找。"""
        result = await self.db.execute(select(self.model).where(getattr(self.model, "id") == id))
        return result.scalar_one_or_none()

    async def find_all(
        self, offset: int = 0, limit: int = 100, **filters: object
    ) -> list[ModelType]:
        """查找所有，支持过滤和分页。"""
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, entity: ModelType) -> ModelType:
        """创建实体。"""
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """删除实体。"""
        await self.db.delete(entity)
        await self.db.flush()

    async def count(self, **filters: object) -> int:
        """计数。"""
        from sqlalchemy import func

        query = select(func.count()).select_from(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        result = await self.db.execute(query)
        return result.scalar() or 0
