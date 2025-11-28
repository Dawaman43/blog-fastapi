from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.deps import get_db
from app.core.security import create_access_token, verify_password
from app.models import Admin, AdminLogin, TokenResponse

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=TokenResponse)
def login(admin_in: AdminLogin, session: Session = Depends(get_db)):
    statement = select(Admin).where(Admin.email == admin_in.email)
    admin = session.exec(statement).first()

    if not admin:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    if not verify_password(admin_in.password, admin.hashed_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token = create_access_token(subject=str(admin.id))
    return {"access_token": token, "token_type": "bearer"}
