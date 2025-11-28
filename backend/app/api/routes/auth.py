from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.deps import get_db
from app.core.security import create_access_token, verify_password
from app.models import Admin, TokenResponse

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token", response_model=TokenResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_db),
):
    admin = session.exec(select(Admin).where(Admin.email == email)).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token = create_access_token(subject=str(admin.id))
    return {"access_token": token, "token_type": "bearer"}
