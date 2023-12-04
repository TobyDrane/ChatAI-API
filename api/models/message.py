import uuid

from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
from pydantic import UUID4


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Message(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    author: Literal["assistant", "user"]
    content: str
    created_at: datetime = Field(default_factory=datetime_now)

    class Config:
        allow_population_by_field_name = True
