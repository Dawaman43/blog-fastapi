import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Blog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=3, index=True, max_length=100)
    description: str = Field(min_length=5)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    admin_id: uuid.UUID = Field(foreign_key="admin.id")
    admin: Optional["Admin"] = Relationship(back_populates="blogs")


class Admin(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = Field(default=True)
    username: Optional[str] = Field(default=None)
    hashed_password: str
    blogs: List["Blog"] = Relationship(
        back_populates="admin", sa_relationship_kwargs={"cascade": "all,delete"}
    )


class TokenPayload(BaseModel):
    sub: str | None = None


class AdminCreate(SQLModel):
    email: EmailStr
    username: str
    password: str


class AdminPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    username: Optional[str]
    is_superuser: bool


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
