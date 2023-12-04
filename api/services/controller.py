from typing import Generator, Any
from pymongo.database import Database
from fastapi.responses import Response
from fastapi import status as http_status

from api.adapters.openai_adapter import (
    generate_chat_completion,
    generate_chat_completion_stream,
)
from api.adapters.mongodb_adapter import insert_conversation_message

from api.models.conversation import ConversationCompletionRequest
from api.models.message import Message


def conversation_message_completion_stream(
    conversation_completion_request: ConversationCompletionRequest,
    conversation_id: str,
    db: Database,
) -> Generator[str, Any, None]:
    message_tokens = ""
    for token in generate_chat_completion_stream(conversation_completion_request):
        yield token
        message_tokens += token

    message = Message(author="assistant", content=message_tokens)
    insert_conversation_message(db, message, conversation_id)


def conversation_messsage_completion(
    conversation_completion_request: ConversationCompletionRequest,
    conversation_id: str,
    db: Database,
) -> Message:
    chat_completion = generate_chat_completion(conversation_completion_request)
    choices = chat_completion.choices
    if len(choices) > 0:
        choice = choices[0]
        message = Message(author=choice.message.role, content=choice.message.content)
        insert_conversation_message(db, message, conversation_id)

        return message

    return Response(status_code=http_status.HTTP_204_NO_CONTENT)
