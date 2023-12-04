from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from api.models.conversation import Conversation, ConversationCompletionRequest
from api.models.message import Message

from api.services.controller import (
    conversation_messsage_completion,
    conversation_message_completion_stream,
)

from api.adapters.mongodb_adapter import (
    get_mongo_db_from_request,
    insert_conversation,
    get_all_conversations,
    insert_conversation_message,
)

conversation_router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
    responses={404: {"description": "Not found"}},
)


@conversation_router.get("")
async def get_conversations(request: Request) -> list[Conversation]:
    db = get_mongo_db_from_request(request)
    return get_all_conversations(db)


@conversation_router.post("")
async def create_conversation(request: Request) -> Conversation:
    db = get_mongo_db_from_request(request)
    return insert_conversation(db)


@conversation_router.post("/completion/{conversation_id}")
async def create_conversation_completion(
    request: Request,
    conversation_completion_request: ConversationCompletionRequest,
    conversation_id: str,
):
    db = get_mongo_db_from_request(request)
    # Insert the users message into the DB
    message = Message(author="user", content=conversation_completion_request.message)
    insert_conversation_message(db, message, conversation_id)

    if conversation_completion_request.stream:
        generator = conversation_message_completion_stream(
            conversation_completion_request, conversation_id, db
        )
        return StreamingResponse(generator, media_type="text/plain")

    return conversation_messsage_completion(
        conversation_completion_request, conversation_id, db
    )
