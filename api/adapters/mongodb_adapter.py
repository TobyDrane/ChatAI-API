import os

from uuid import UUID
from fastapi import Request
from pymongo import MongoClient
from pymongo.database import Database

from api.models.message import Message
from api.models.conversation import Conversation

DB_NAME = os.environ.get("DB")


def get_mongo_db_from_request(request: Request) -> Database:
    mongo_client: MongoClient = request.app.mongodb_client
    return mongo_client.get_database(DB_NAME)


def insert_conversation(db: Database) -> Conversation:
    try:
        conversations = db.get_collection("conversations")
        conversation = Conversation()
        conversations.insert_one(conversation.model_dump())
        return conversation
    except Exception as e:
        print(f"Error inserting conversation {e}")


def get_all_conversations(db: Database) -> list[Conversation]:
    conversations = db.get_collection("conversations")
    return list(conversations.find({}))


def insert_conversation_message(db: Database, message: Message, conversation_id: str):
    conversations = db.get_collection("conversations")
    try:
        query = {"id": UUID(conversation_id)}
        update_result = conversations.update_one(
            query, {"$push": {"messages": message.model_dump()}}
        )
        if update_result.modified_count == 0:
            raise Exception(f"Conversation with {conversation_id} not found")
    except Exception as e:
        print(f"Error inserting message into conversation {e}")
