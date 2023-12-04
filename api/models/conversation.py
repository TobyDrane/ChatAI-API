import uuid

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import UUID4

from api.models.message import Message


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Conversation(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    messages: Optional[list[Message]] = []
    created_at: datetime = Field(default_factory=datetime_now)

    class Config:
        allow_population_by_field_name = True


class ConversationCompletionRequest(BaseModel):
    message: str
    stream: Optional[bool] = False

    def generate_message_payload(self) -> dict:
        return {"payload": self.message}
