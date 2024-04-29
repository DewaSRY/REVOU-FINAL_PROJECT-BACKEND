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


class TestCreateUserImage(MockDatabaseConnection):
    def setup_class(self):
        super().setup_class(self)
        UserTypeModel.clean_all_model()
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()
        UserImageModel.clean_all_model()

    def setUp(self) -> None:
        self.type_user = UserTypeModel.add_model(name="some type")
        self.user_create: UserModel = UserModel.add_model(
            username="some name another one",
            password="some email another email",
            email="some password",
        )

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        UserTypeModel.clean_all_model()
        UserImageModel.clean_all_model()

    def test_put_image_as_profile(self):
        img_secure_url = "some secure Url"
        img_secure_url_two = "some secure Url two"

        default_user_profile_url = self.user_create.profile_url
        UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url,
            public_id=str(uuid4()),
        )
        user_profile_after_first_create = self.user_create.profile_url
        second_image = UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url_two,
            public_id=str(uuid4()),
        )
        user_profile_after_second_create = self.user_create.profile_url
        assert default_user_profile_url == ""
        assert user_profile_after_first_create == img_secure_url
        assert user_profile_after_second_create == img_secure_url
        UserImageModel.put_as_profile(image_id=second_image.id)

        assert second_image.secure_url == self.user_create.profile_url

    def test_create_user_image(self):
        img_secure_url = "some secure Url"
        img_secure_url_two = "some secure Url two"

        default_user_profile_url = self.user_create.profile_url
        UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url,
            public_id=str(uuid4()),
        )
        user_profile_after_first_create = self.user_create.profile_url
        UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url_two,
            public_id=str(uuid4()),
        )
        user_profile_after_second_create = self.user_create.profile_url

        assert default_user_profile_url == ""
        assert user_profile_after_first_create == img_secure_url
        assert user_profile_after_second_create == img_secure_url

    def test_get_user_image(self):
        img_secure_url = "some secure Url"
        img_public_id = str(uuid4())
        create_image = UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url,
            public_id=img_public_id,
        )
        get_image = UserImageModel.get_model_by_id(model_id=create_image.id)
        assert create_image == get_image

    def test_delete_user_image(self):
        img_secure_url = "some secure Url"
        img_public_id = str(uuid4())
        create_image = UserImageModel.add_model(
            user_id=self.user_create.id,
            secure_url=img_secure_url,
            public_id=img_public_id,
        )
        image_id = create_image.id
        imageDelete = UserImageModel.delete_model_by_id(model_id=image_id)
        get_image = UserImageModel.get_model_by_id(model_id=image_id)

        assert create_image == imageDelete
        assert create_image != get_image
