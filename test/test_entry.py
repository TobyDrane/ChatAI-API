from test.base_test_controller import BaseClientTest


class TestStatus(BaseClientTest):
    def test_status_is_200(self):
        response = self.client.get("/")
        assert response.status_code == 200
