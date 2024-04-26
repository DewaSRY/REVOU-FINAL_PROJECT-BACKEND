"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.user import (
    UserTypeModel,
    UserImageModel,
    UserModel,
)
from pprint import pprint


class TestCreateUSer(MockDatabaseConnection):
    def setup_class(self):
        super().setup_class(self)
        UserTypeModel.clean_all_model()
        self.type_user = UserTypeModel.add_model(name="some type")
        self.user_name = "some name another one"
        self.user_email = "some email another email"
        self.user_password = "some password"

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()

    def test_create_user(self):
        user_create = UserModel.add_model(
            username=self.user_name, password=self.user_password, email=self.user_email
        )
        # pprint(UserTypeModel.get_all_model(), indent=2)

        assert user_create.email == self.user_email
        assert user_create.username == self.user_name
        assert user_create.password != self.user_password
        assert user_create.match_password(self.user_password) == True
        assert user_create.user_type_id == self.type_user.id
        assert user_create.user_type == self.type_user.name

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
            assert str(e) == f"username: {self.user_name} already use"

    def test_create_with_same_username(self):
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
            pprint(str(e))
            assert str(e) == f"email: {self.user_email} already use"
