from unittest.mock import Mock, patch, call
from pytest_httpx import HTTPXMock

from api.services.controller import (
    conversation_message_completion_stream,
    conversation_messsage_completion,
)

from api.models.conversation import ConversationCompletionRequest
from api.models.openai_api import ChatCompletionResponse


def test_conversation_message_completion_stream(
    httpx_mock: HTTPXMock,
):
    db_mock = Mock()
    chat_completion_response = ChatCompletionResponse(
        choices=[
            {
                "index": 0,
                "message": {"content": "x", "role": "assistant"},
                "finish_reason": "stop",
            }
        ],
        model="test",
        system_fingerprint="test",
        usage={"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
    )
    httpx_mock.add_response(json=chat_completion_response.model_dump())
    request = ConversationCompletionRequest(message="Some test message", stream=True)

    stream = conversation_message_completion_stream(
        request, "f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2", db_mock
    )
    for token in stream:
        assert token == "x"

    assert db_mock.get_collection.return_value.update_one.call_count == 1


def test_conversation_message_completion(httpx_mock: HTTPXMock):
    db_mock = Mock()
    chat_completion_response = ChatCompletionResponse(
        choices=[
            {
                "index": 0,
                "message": {"content": "x", "role": "assistant"},
                "finish_reason": "stop",
            }
        ],
        model="test",
        system_fingerprint="test",
        usage={"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
    )
    httpx_mock.add_response(json=chat_completion_response.model_dump())
    request = ConversationCompletionRequest(message="Some test message", stream=False)

    message = conversation_messsage_completion(
        request, "f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2", db_mock
    )
    assert message.author == "assistant"
    assert message.content == "x"
    assert db_mock.get_collection.return_value.update_one.call_count == 1
