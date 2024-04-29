"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.user import (
    UserTypeModel,
    UserModel,
)
from pprint import pprint
from unittest import skip
from uuid import uuid4


class TestCreateUser(MockDatabaseConnection):
    def setup_class(self):
        super().setup_class(self)
        UserTypeModel.clean_all_model()
        self.user_name = "some name another one"
        self.user_email = "some email another email"
        self.user_password = "some password"
        self.name_list = [
            "one",
            "two",
            "three",
            "four",
            "five",
        ]

    def setUp(self) -> None:
        self.type_user = UserTypeModel.add_model(name="some type")

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()

    # @skip("just skip")
    def test_create_user(self):
        user_create: UserModel = UserModel.add_model(
            username=self.user_name, password=self.user_password, email=self.user_email
        )
        # pprint(UserTypeModel.get_all_model(), indent=2)
        # pprint(user_create, indent=2)
        assert user_create.email == self.user_email
        assert user_create.username == self.user_name
        assert user_create.password != self.user_password
        assert user_create.match_password(self.user_password) == True
        assert user_create.user_type_id == self.type_user.id
        assert user_create.user_type == self.type_user.name

    def test_get_user_by_email_or_username(self):
        user_create: UserModel = UserModel.add_model(
            username=self.user_name, password=self.user_password, email=self.user_email
        )
        by_username: UserModel = UserModel.get_by_email_or_username(
            username=self.user_name, email="100"
        )
        by_email: UserModel = UserModel.get_by_email_or_username(
            username="100", email=self.user_email
        )
        by_nothing: UserModel = UserModel.get_by_email_or_username(
            username="nothing", email="nothing"
        )
        # pprint(UserTypeModel.get_all_model(), indent=2)
        # pprint(user_create, indent=2)
        assert by_username == user_create
        assert by_email == user_create
        assert bool(by_nothing) == False

    # @skip("just skip")
    def test_create_with_same_username(self):
        try:
            UserModel.add_model(
                username=self.user_name,
                password=self.user_password,
                email="another email",
            )
            UserModel.add_model(
                username=self.user_name,
                password=self.user_password,
                email="another email",
            )
        except Exception as e:
            assert str(e) == f"username: '{self.user_name}' already use"

    # @skip("just skip")
    def test_create_email_same_username(self):
        try:
            UserModel.add_model(
                username=self.user_name,
                password=self.user_password,
                email=self.user_email,
            )
            UserModel.add_model(
                username="some another user name",
                password=self.user_password,
                email=self.user_email,
            )
        except Exception as e:
            assert str(e) == f"email: '{self.user_email}' already use"

    def test_get_user_by_email(self):

        user_create = UserModel.add_model(
            username=self.user_name,
            password=self.user_password,
            email=self.user_email,
        )

        for index in range(len(self.name_list)):
            UserModel.add_model(
                username=self.name_list[index],
                email="{}@gmail.com".format(self.name_list[index]),
                password=self.name_list[index],
            )
        userMatch = UserModel.get_by_email_or_username(email=self.user_email)

        assert user_create == userMatch

    def test_get_user_by_username(self):

        user_create = UserModel.add_model(
            username=self.user_name,
            password=self.user_password,
            email=self.user_email,
        )
        for index in range(len(self.name_list)):
            UserModel.add_model(
                username=self.name_list[index],
                email="{}@gmail.com".format(self.name_list[index]),
                password=self.name_list[index],
            )
        userMatch = UserModel.get_by_email_or_username(username=self.user_name)
        assert user_create == userMatch
