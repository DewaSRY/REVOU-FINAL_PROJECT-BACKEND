"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.user import (
    UserTypeModel,
    UserImageModel,
    UserModel,
    UserUpdateData,
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

        self.phone_number = "phone_number"
        self.address = "address"
        self.occupation = "occupation"
        self.description = "description"

        self.update_username = "update username"
        self.update_email = "update email"

    def setUp(self) -> None:
        self.type_user = UserTypeModel.add_model(name="some type")
        self.user_create = UserModel.add_model(
            email=self.user_email, username=self.user_name, password=self.user_password
        )

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()
        UserImageModel.clean_all_model()

    def test_update(self):

        user_update = UserModel.update_with_update_data(
            user_id=self.user_create.id,
            update_data=UserUpdateData(
                username=self.update_username,
                email=self.update_email,
                phone_number=self.phone_number,
                address=self.address,
                occupation=self.occupation,
                description=self.description,
            ),
        )
        assert bool(user_update) == True
        assert user_update.username == self.update_username
        assert user_update.id == self.user_create.id

    def test_update_withe_same_email(self):
        user_update = UserModel.update_with_update_data(
            user_id=self.user_create.id,
            update_data=UserUpdateData(
                username=self.update_username,
                email=self.user_create.email,
                phone_number=self.phone_number,
                address=self.address,
                occupation=self.occupation,
                description=self.description,
            ),
        )
        assert bool(user_update) == True

    def test_update_withe_same_username(self):
        user_update = UserModel.update_with_update_data(
            user_id=self.user_create.id,
            update_data=UserUpdateData(
                username=self.user_create.username,
                email=self.update_email,
                phone_number=self.phone_number,
                address=self.address,
                occupation=self.occupation,
                description=self.description,
            ),
        )
        assert bool(user_update) == True

    def test_update_withe_same_username_and_email(self):
        user_update = UserModel.update_with_update_data(
            user_id=self.user_create.id,
            update_data=UserUpdateData(
                username=self.user_create.username,
                email=self.user_create.email,
                phone_number=self.phone_number,
                address=self.address,
                occupation=self.occupation,
                description=self.description,
            ),
        )
        assert bool(user_update) == True
