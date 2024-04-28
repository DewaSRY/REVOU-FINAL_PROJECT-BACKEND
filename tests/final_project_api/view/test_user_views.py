"""_summary_
"""

from tests.mock_flask import MockFlask
from werkzeug.test import TestResponse
from pprint import pprint
from unittest import skip
from app.final_project_api.model.user import UserModel


class TestUserViews(MockFlask):

    def tearDown(self) -> None:
        UserModel.clean_all_model()

    def test_user_register(self):
        response: TestResponse = self.client.post(
            "user/register",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        # pprint("")
        # pprint(response.get_json(), indent=2)
        assert bool(response.get_json()) == True

    def test_user_login(self):
        self.client.post(
            "user/register",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        response: TestResponse = self.client.post(
            "user/login",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        # pprint("")
        # pprint(response.get_json(), indent=2)
        assert bool(response.get_json()) == True

    def test_user_sign_in(self):
        register_response: TestResponse = self.client.post(
            "user/register",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        response: TestResponse = self.client.get(
            "user/sign-in",
            headers={
                "content-type": "multipart/form-data",
                "accept": "application/json",
                "Authorization": "Bearer "
                + register_response.get_json()["access_token"],
            },
        )
        # pprint("")
        # pprint(response.get_json(), indent=2)
        # pprint(register_response.get_json(), indent=2)
        assert bool(response.get_json()) == True

    def test_user_sign_in(self):
        register_response: TestResponse = self.client.post(
            "user/register",
            json={
                "username": "testing register user name",
                "password": "register password",
                "email": "someEmail@gmail.com",
            },
        )
        response: TestResponse = self.client.put(
            "/user",
            json={
                "username": "testing register user name",
                "email": "someEmail@gmail.com",
                "phone_number": "phone_number",
                "address": "address",
                "occupation": "occupation",
                "description": "description",
            },
            headers={
                "accept": "application/json",
                "Authorization": "Bearer "
                + register_response.get_json()["access_token"],
            },
        )
        # pprint(response.get_json(), indent=2)
        # pprint(register_response.get_json(), indent=2)
        assert bool(response.get_json()) == True
