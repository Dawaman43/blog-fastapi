from app.models import Admin, Blog
from sqlmodel import Session


def create_blog(*, session: Session, admin: Admin, new_blog: Blog) -> Blog:
    db_obj = Blog(
        title=new_blog.title, description=new_blog.description, admin_id=admin.id
    )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj
