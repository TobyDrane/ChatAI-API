from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import status as http_status

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
    check_conversation_exists,
)

conversation_router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
    responses={404: {"description": "Not found"}},
)


@conversation_router.get("")
async def get_conversations(request: Request) -> list[Conversation]:
    """
    ## List all conversations

    Use this endpoint to retrieve a list of all current conversation with the database.
    This also includes all the messages in each conversation and for large amounts of data
    may be slow.

    ### Click  `Try it out` to use the endpoint

    """  # noqa: E501
    db = get_mongo_db_from_request(request)
    return get_all_conversations(db)


@conversation_router.post("")
async def create_conversation(request: Request) -> Conversation:
    """
    ## Create new conversation

    Use this endpoint to create a new blank conversation within the database. Once a conversation
    is created the user can chat to the AI for the given conversation.

    ### Click  `Try it out` to use the endpoint

    """  # noqa: E501
    db = get_mongo_db_from_request(request)
    return insert_conversation(db)


@conversation_router.post("/completion/{conversation_id}")
async def create_conversation_completion(
    request: Request,
    conversation_completion_request: ConversationCompletionRequest,
    conversation_id: str,
):
    """
    ## Conversation chat completion

    Using this endpoint you can chat to the AI for a given conversation. The AI will respond with
    a message based on the users input. All messages via this endpoint are stored within the database.

    ### Inputs

    | Parameters                        | Usage               | Example values   | Definition                                      |
    |-----------------------------------|---------------------|------------------|-------------------------------------------------|
    | `conversation_id`                 | URL Parameter       |                  | The conversation ID string                      |
    | `conversation_completion_request` | JSON Request Body   | See below        | The chat completion request model               |

    ```json
    {
            "message": "How would I create a chocolate cake?",
            "stream": "true",
    }
    ```

    ### Click  `Try it out` to use the endpoint
    """  # noqa: E501
    db = get_mongo_db_from_request(request)

    if not check_conversation_exists(db, conversation_id):
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

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
