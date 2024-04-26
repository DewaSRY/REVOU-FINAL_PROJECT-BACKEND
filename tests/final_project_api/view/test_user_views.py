"""_summary_
"""

from tests.mock_flask import MockFlask

from pprint import pprint


class TestUserViews(MockFlask):
    def test_first(self):
        assert 1 == 1

    def test_user_register(self):
        with self.app.app_context():
            response = self.client.post(
                "user/register",
                json={
                    "username": "testing register user name",
                    "password": "register password",
                    "email": "someEmail@gmail.com",
                },
            )
            pprint(response.get_json(), indent=2)
