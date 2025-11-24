from app import crud
from app.core.config import Settings
from app.models import Admin
from sqlmodel import Session, create_engine, select

from backend.app.utils import hash_password

engine = create_engine(str(Settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    existing_admin = session.exec(select(Admin)).first()
    if not existing_admin:
        admin = Admin(
            email="admin@gmail.com",
            username="admin",
            is_superuser=True,
            hashed_password=hash_password("12345678"),
        )

        print("Default admin created.")
    else:
        print("Admin already exists — skipping.")
