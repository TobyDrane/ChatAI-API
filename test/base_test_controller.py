from abc import ABC
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.entry import app


class BaseClientTest(ABC):
    client = None

    @classmethod
    def setup_class(cls):
        app.mongodb_client = Mock()
        app.mongodb_client.get_database.return_value = "DB_TEST"

        cls.client = TestClient(app, raise_server_exceptions=False)
