"""Authentication endpoints。"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.exceptions import ValidationException
from app.core.security import decode_token
from app.schemas.user import LoginRequest, RefreshRequest, UserCreate, UserWithToken
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserWithToken:
    """注册新用户。"""
    service = AuthService(db)
    user = await service.register(data)
    tokens = await service.generate_tokens(user)
    return tokens


@router.post("/login", response_model=UserWithToken)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)) -> UserWithToken:
    """用户登录。"""
    service = AuthService(db)
    tokens = await service.authenticate(data.email, data.password)
    return tokens


@router.post("/refresh", response_model=dict)
async def refresh_token(data: RefreshRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """刷新 access token。"""
    try:
        payload = decode_token(data.refresh_token)
    except ValueError as exc:
        raise ValidationException(str(exc)) from exc
    if payload.get("type") != "refresh" or not payload.get("sub"):
        raise ValidationException("A valid refresh token is required.")
    service = AuthService(db)
    new_token = await service.refresh_access_token(str(payload["sub"]))
    return {"access_token": new_token, "token_type": "bearer"}
