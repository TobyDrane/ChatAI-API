from uuid import UUID
from unittest.mock import patch, Mock

from test.base_test_controller import BaseClientTest
from api.models.conversation import Conversation
from api.models.message import Message


class TestConversation(BaseClientTest):
    @patch("api.controller.conversation.get_all_conversations")
    @patch("api.controller.conversation.get_mongo_db_from_request")
    def test_get_conversations(
        self, mock_get_mongo_db_from_request, mock_get_all_conversations
    ):
        mock_get_mongo_db_from_request.return_value = Mock()
        mock_get_all_conversations.return_value = [
            Conversation(id=UUID("f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2"))
        ]
        response = self.client.get("/conversation")
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 1
        assert response_data[0]["id"] == "f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2"

    @patch("api.controller.conversation.insert_conversation")
    @patch("api.controller.conversation.get_mongo_db_from_request")
    def test_create_conversation(
        self, mock_get_mongo_db_from_request, mock_insert_conversation
    ):
        mock_get_mongo_db_from_request.return_value = Mock()
        mock_insert_conversation.return_value = Conversation(
            id=UUID("f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2")
        )
        response = self.client.post("/conversation")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == "f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2"

    @patch("api.controller.conversation.insert_conversation_message")
    @patch("api.controller.conversation.get_mongo_db_from_request")
    @patch("api.controller.conversation.conversation_messsage_completion")
    def test_create_conversation_completion(
        self,
        mock_conversation_message_completion,
        mock_get_mongo_db_from_request,
        mock_insert_conversation_message,
    ):
        mock_get_mongo_db_from_request.return_value = Mock()
        mock_insert_conversation_message.return_value = None
        mock_conversation_message_completion.return_value = Message(
            author="assistant", content="Hi"
        )
        response = self.client.post(
            "/conversation/completion/f7eec0cd-96e1-4793-b1d3-2c1d7c4580d2",
            json={
                "message": "Hello",
                "stream": False,
            },
        )
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["content"] == "Hi"
        assert response_data["author"] == "assistant"
