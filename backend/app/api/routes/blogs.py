from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import app.crud as crud
from app.api.deps import get_current_Admin, get_db
from app.models import Admin, Blog

router = APIRouter(prefix="/blogs", tags=["blog"])


@router.get("/", response_model=List[Blog])
def get_blogs(session: Session = Depends(get_db)):
    return crud.get_blogs(session=session)


@router.post("/", response_model=Blog, status_code=status.HTTP_201_CREATED)
def create_blog(
    title: str,
    description: str,
    session: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_Admin),
):
    new_blog = Blog(title=title, description=description, admin_id=current_admin.id)
    return crud.create_blog(session=session, admin=current_admin, new_blog=new_blog)


@router.get("/{blog_id}", response_model=Blog)
def get_blog(blog_id: UUID, session: Session = Depends(get_db)):
    blog = crud.get_blog_by_id(session=session, id=blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not FileNotFoundError")
    return blog


@router.put("/{blog_id}", response_model=Blog)
def update_blog(
    title: str,
    description: str,
    blog_id: UUID,
    session: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_Admin),
):
    blog = Blog(title=title, description=description, admin_id=current_admin.id)
    return crud.update_blog(session=session, blog=blog, id=blog_id)


@router.delete("/{blog_id}", response_model=Blog)
def delete_blog(blog_id: UUID, session: Session = Depends(get_db)):
    return crud.delete_blog(id=blog_id, session=session)
