from collections.abc import Generator
from typing import Annotated, Any, cast

import jwt
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import Admin, TokenPayload
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_v1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_Admin(session: SessionDep, token: TokenDep) -> Admin:
    try:
        payload = security.decode_access_token(token)
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token payload"
            )
        token_data = TokenPayload(**payload)

    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.sub is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token missing subject"
        )
    admin = session.get(Admin, token_data.sub)

    if not admin:
        raise HTTPException(status_code=404, detail="User not found")
    return admin


CurrentAdmin = Annotated[Admin, Depends(get_current_Admin)]
