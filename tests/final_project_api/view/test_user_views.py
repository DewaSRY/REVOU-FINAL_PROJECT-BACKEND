"""_summary_
"""

from tests.mock_flask import MockFlask
from werkzeug.test import TestResponse
from pprint import pprint


class TestUserViews(MockFlask):
    def test_first(self):
        assert 1 == 1

    def test_user_register(self):
        """
            with self.app.test_client() as client:
        client.post('/v0/scenes/test/foo',
                    data=dict(image=(StringIO('fake image'), 'image.png')),
                    headers={'content-md5': 'some hash'});
        """
        response: TestResponse = self.client.post(
            "user/register",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        pprint("\nRegister response")
        pprint(response.get_json(), indent=2)
