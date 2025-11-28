from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

import app.crud as crud
from app.api.deps import get_db
from app.models import Admin, AdminCreate, AdminPublic

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/", response_model=List[AdminPublic])
def get_admins(session: Session = Depends(get_db)) -> List[AdminPublic]:
    admins = crud.get_admins(session=session)
    return [AdminPublic.model_validate(a) for a in admins]


@router.post("/", response_model=AdminPublic)
def create_admin(
    admin_in: AdminCreate, session: Session = Depends(get_db)
) -> AdminPublic:
    existing = session.exec(select(Admin).where(Admin.email == admin_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")
    admin = crud.create_admin(session=session, admin_in=admin_in)
    return AdminPublic.model_validate(admin)
