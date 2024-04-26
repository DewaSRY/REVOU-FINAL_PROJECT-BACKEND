"""_summary_
"""

from app.final_project_api.model.user import LoginSchemas, AuthData
from unittest import TestCase
from pprint import pprint


class TestLoginSchema(TestCase):

    def test_create_login_schema_one(self):
        login_schema = LoginSchemas()
        username_test = "some user name"
        user_password_test = "some password"

        login_data: AuthData = login_schema.load(
            {"username": username_test, "password": user_password_test}
        )
        assert login_data.username == username_test
        assert login_data.password == user_password_test
        assert login_data.email == ""

    def test_create_login_schema_two(self):
        login_schema = LoginSchemas()
        email_test = "some@gmail.com"
        user_password_test = "some password"

        login_data: AuthData = login_schema.load(
            {"email": email_test, "password": user_password_test}
        )

        assert login_data.username == ""
        assert login_data.password == user_password_test
        assert login_data.email == email_test
