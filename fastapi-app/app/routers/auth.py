"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database import get_user_collection
from ..repositories.user_repository import UserRepository
from ..schemas.user import Token, UserCreate, UserLogin
from ..services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_repo(collection: AsyncIOMotorCollection = Depends(get_user_collection)) -> UserRepository:
    """Provide a user repository dependency."""
    return UserRepository(collection)


@router.post("/register", response_model=str)
async def register(user: UserCreate, repo: UserRepository = Depends(get_user_repo)) -> str:
    """Create a new user and return the username."""
    existing = await repo.get_by_username(user.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return await register_user(repo, user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, repo: UserRepository = Depends(get_user_repo)) -> Token:
    """Authenticate a user and return a JWT token."""
    token = await authenticate_user(repo, user.username, user.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=token)
