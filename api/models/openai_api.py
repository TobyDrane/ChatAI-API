import shortuuid
import time

from typing import Optional, Literal
from pydantic import BaseModel, Field


class DeltaMessage(BaseModel):
    role: str
    content: Optional[str] = Field(default="")


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = Field(default="")


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[Literal["stop", "length"]] = None


class ChatCompletionUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class ChatCompletionStreamResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{shortuuid.random()}")
    choices: list[ChatCompletionResponseStreamChoice]
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    object: str = "chat.completion.chunk"


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{shortuuid.random()}")
    choices: list[ChatCompletionResponseChoice]
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    system_fingerprint: str
    object: str = "chat.completion"
    usage: ChatCompletionUsage
