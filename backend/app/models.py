import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Blog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=3, index=True, max_length=100)
    description: str = Field(min_length=5)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    admin_id: uuid.UUID = Field(foreign_key="admin.id")
    admin: Optional["Admin"] = Relationship(back_populates="blogs")


class Admin(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = Field(default=True)
    username: Optional[str] = Field(default=None)
    blogs: List["Blog"] = Relationship(back_populates="admin")
    hashed_password: str


class TokenPayload(SQLModel):
    sub: str | None = None
