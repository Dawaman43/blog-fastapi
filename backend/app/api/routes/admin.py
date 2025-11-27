from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Admin, AdminCreate
from app.api.deps import get_db
import app.crud as crud

router = APIRouter(prefix="/admin", tags=["tags"])

@router.get("/", response_model=List[Admin])
def get_admins(session: Session = Depends(get_db))->List[Admin]:
    return crud.get_admins(session=session)

@router.post("/", response_model=Admin)
def create_admin(admin_id: AdminCreate, session:Session = Depends(get_db)):
    existing = session.exec(select(Admin).where(Admin.email == admin_id.email))
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")
    return crud.create_admin(session=session, admin_id=admin_id)
