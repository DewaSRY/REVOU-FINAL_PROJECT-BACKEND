"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.user import (
    UserTypeModel,
    UserImageModel,
    UserModel,
)
from pprint import pprint
from unittest import skip
from uuid import uuid4


class TestCreateUSer(MockDatabaseConnection):
    def setup_class(self):
        super().setup_class(self)
        UserTypeModel.clean_all_model()
        self.user_name = "some name another one"
        self.user_email = "some email another email"
        self.user_password = "some password"

    def setUp(self) -> None:
        self.type_user = UserTypeModel.add_model(name="some type")

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()
        UserImageModel.clean_all_model()

    def test_create_user_image(self):
        img_secure_url = "some secure Url"
        img_secure_url_two = "some secure Url two"
        user_create: UserModel = UserModel.add_model(
            username=self.user_name, password=self.user_password, email=self.user_email
        )
        default_user_profile_url = user_create.profile_url
        UserImageModel.add_model(
            user_id=user_create.id, secure_url=img_secure_url, public_id=str(uuid4())
        )
        user_profile_after_first_create = user_create.profile_url
        UserImageModel.add_model(
            user_id=user_create.id,
            secure_url=img_secure_url_two,
            public_id=str(uuid4()),
        )
        user_profile_after_second_create = user_create.profile_url

        assert default_user_profile_url == ""
        assert user_profile_after_first_create == img_secure_url
        assert user_profile_after_second_create == img_secure_url
        assert img_secure_url in user_create.user_images
        assert img_secure_url_two in user_create.user_images

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

    @skip("just skip")
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
            assert str(e) == f"email: '{self.user_email}' already use"
