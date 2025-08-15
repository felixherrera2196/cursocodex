"""Service layer for authentication logic."""
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from ..repositories.user_repository import UserRepository
from ..models.user import UserInDB
from ..schemas.user import UserCreate

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def register_user(repo: UserRepository, user: UserCreate) -> str:
    """Register a new user and return the username."""
    hashed = hash_password(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed)
    return await repo.create(user_in_db)


async def authenticate_user(repo: UserRepository, username: str, password: str) -> Optional[str]:
    """Authenticate a user and return a JWT token if successful."""
    user = await repo.get_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_access_token({"sub": user.username})
