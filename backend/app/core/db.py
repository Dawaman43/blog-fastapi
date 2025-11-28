from this import s
from app import crud
from app.core.config import settings
from app.models import Admin
from sqlmodel import Session, create_engine, select

from app.utils import hash_password

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db() -> None:
    with Session(engine) as session:
        existing_admin = session.exec(select(Admin)).first()
        if not existing_admin:
            admin = Admin(
                email="admin@gmail.com",
                username="admin",
                is_superuser=True,
                hashed_password=hash_password("12345678"),
            )

            session.add(admin)
            session.commit()

            print("Default admin created.")
        else:
            print("Admin already exists — skipping.")


if __name__ == "__main__":
    init_db()
