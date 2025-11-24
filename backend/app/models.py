import uuid

from sqlmodel import Field, SQLModel


class Blog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=3, index=True, max_length=100)
    description: str = Field(min_length=5)
