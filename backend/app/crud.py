from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core import security
from app.models import Admin, AdminCreate, Blog


def create_blog(*, session: Session, admin: Admin, new_blog: Blog) -> Blog:
    db_obj = Blog(
        title=new_blog.title, description=new_blog.description, admin_id=admin.id
    )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def get_blogs(*, session: Session) -> List[Blog]:
    statement = select(Blog)
    results = session.exec(statement)
    all_blogs = list(results.all())
    return all_blogs


def get_blog_by_id(*, session: Session, id: UUID) -> Optional[Blog]:
    statement = select(Blog).where(Blog.id == id)
    result = session.exec(statement).first()
    return result


def update_blog(*, session: Session, blog: Blog, id: UUID) -> Blog:
    statement = select(Blog).where(Blog.id == id)
    existing_blog = session.exec(statement).first()

    if not existing_blog:
        raise HTTPException(status_code=404, detail="No blog found with the given id")

    existing_blog.title = blog.title
    existing_blog.description = blog.description

    existing_blog.updated_at = datetime.now(timezone.utc)

    session.add(existing_blog)
    session.commit()
    session.refresh(existing_blog)

    return existing_blog


def delete_blog(*, session: Session, id: UUID) -> Blog:
    statement = select(Blog).where(Blog.id == id)
    blog_to_delete = session.exec(statement).first()

    if not blog_to_delete:
        raise HTTPException(status_code=404, detail="Blog not found")

    session.delete(blog_to_delete)
    session.commit()

    return blog_to_delete


"""
    Admin routes
"""


def get_admins(*, session: Session) -> List[Admin]:
    statement = select(Admin)
    result = session.exec(statement)
    return list(result.all())


def create_admin(*, session: Session, admin_in: AdminCreate) -> Admin:
    hash_password = security.create_password_hash(admin_in.password)

    new_obj = Admin(
        email=admin_in.email, username=admin_in.username, hashed_password=hash_password
    )

    session.add(new_obj)
    session.commit()
    session.refresh(new_obj)

    return new_obj
