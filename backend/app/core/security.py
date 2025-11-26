from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from app.core.config import settings
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

def decode_access_token(token: str)-> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token Expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid Token")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_token_subject(token: str) -> str | None:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload
        raise ValueError("Token payload missing 'sub' ")
    return payload.get("sub")
