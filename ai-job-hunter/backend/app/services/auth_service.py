"""Authentication 业务逻辑。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, ValidationException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserWithToken


class AuthService:
    """认证服务 — 处理注册、登录、token 生成。"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        """注册新用户。"""
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise ConflictException(f"Email '{data.email}' is already registered.")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> UserWithToken:
        """验证凭据并返回 token。"""
        user = await self.repo.find_by_email(email)
        if not user or not user.hashed_password:
            raise ValidationException("Invalid email or password.")
        if not verify_password(password, user.hashed_password):
            raise ValidationException("Invalid email or password.")
        if not user.is_active:
            raise ValidationException("Account is disabled.")

        return await self.generate_tokens(user)

    async def generate_tokens(self, user: User) -> UserWithToken:
        """为用户生成 access + refresh token。"""
        access = create_access_token({"sub": user.id, "role": user.role.value})
        refresh = create_refresh_token({"sub": user.id})
        return UserWithToken(
            user=UserRead.model_validate(user),
            access_token=access,
            refresh_token=refresh,
        )

    async def refresh_access_token(self, user_id: str) -> str:
        """使用 refresh token 获取新的 access token。"""
        user = await self.repo.find_by_id(user_id)
        if not user or not user.is_active:
            raise ValidationException("Invalid user.")
        return create_access_token({"sub": user.id, "role": user.role.value})
