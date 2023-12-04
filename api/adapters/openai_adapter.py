import os
import httpx
import time
from typing import Any, Dict

from api.models.openai_api import (
    ChatCompletionResponse,
)  # , ChatCompletionStreamResponse
from api.models.conversation import ConversationCompletionRequest

URL = os.getenv("OPENAI_URL", "http://localhost:8080")


def generate_chat_completion_steam(request: ConversationCompletionRequest):
    with httpx.Client() as client:
        response = client.post(
            f"{URL}/v1/chat/completions", json=request.generate_message_payload()
        )
        content = ChatCompletionResponse(**response.json())
        choices = content.choices
        if len(choices) > 0:
            message = choices[0].message.content
            for token in message:
                yield token
                time.sleep(0.01)


def generate_chat_completion(
    request: ConversationCompletionRequest,
) -> ChatCompletionResponse:
    with httpx.Client() as client:
        response = client.post(
            f"{URL}/v1/chat/completions", json=request.generate_message_payload()
        )
        return ChatCompletionResponse(**response.json())
