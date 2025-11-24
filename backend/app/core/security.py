from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from app.core.config import settings
from passlib.context import CryptContext

from backend.app.api.deps import jwt_typed

pwd_context = CryptContext(schemes=["bcrypt"], depricated="auto")

ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt_typed(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
