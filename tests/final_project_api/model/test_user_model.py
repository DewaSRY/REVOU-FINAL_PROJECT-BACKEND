"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.user import (
    UserTypeModel,
    UserImageModel,
    UserModel,
)
from pprint import pprint


class TestUserModel(MockDatabaseConnection):

    def setup_class(self):
        super().setup_class(self)
        self.user_type_one = UserTypeModel.add_model(UserTypeModel("model one"))

    def teardown_class(self):
        UserModel.clean_all_model()
        UserTypeModel.delete_model(self.user_type_one)
        UserImageModel.clean_all_model()

    def test_create_first_user(self):
        userName = "some name"
        userPassword = "some password"
        userEmail = "some Email"
        user_create = UserModel.add_model(
            username=userName, email=userEmail, password=userPassword
        )
        assert user_create.user_type_id == self.user_type_one.id
        assert user_create.password != userPassword
        assert user_create.match_password(userPassword) == True
        assert user_create.user_type == self.user_type_one.name

    def test_update_first_user(self):
        userName = "some name to update"
        userPassword = "some password to update"
        userEmail = "some Email to update"
        user_create = UserModel.add_model(
            username=userName, email=userEmail, password=userPassword
        )
        assert user_create.user_type_id == self.user_type_one.id
        assert user_create.password != userPassword
        assert user_create.match_password(userPassword) == True

        assert user_create.user_type == self.user_type_one.name
        newUserName = "new name"
        newUSerPassword = "new password"
        neUserEmail = "new email"
        user_get_update: UserModel = UserModel.update_with_id(
            model_id=user_create.id, username=newUserName, email=neUserEmail
        )
        assert user_get_update.username == newUserName
        assert user_get_update.email == neUserEmail
        user_update_password: UserModel = UserModel.update_with_id(
            model_id=user_create.id, password=newUSerPassword
        )
        assert user_update_password.match_password(newUSerPassword)

    def test_user_create_images(self):
        create_user = UserModel.add_model(
            username="create image two",
            email="create image",
            password="create image",
        )

        image_one, image_two, image_three = UserImageModel.add_all_model(
            [
                UserImageModel(image_url="some url", user_id=create_user.id),
                UserImageModel(image_url="some url two", user_id=create_user.id),
                UserImageModel(image_url="some url three", user_id=create_user.id),
            ]
        )
        user_image_one, user_image_two, user_image_three = create_user.user_images
        assert image_one.image_url == user_image_one
        assert image_two.image_url == user_image_two
        assert image_three.image_url == user_image_three

    def test_error_create_same_user_with_same_user_name(self):
        user_create = UserModel.add_model(
            username="create user name",
            email="create email",
            password="create password",
        )
        try:
            same_user = UserModel.add_model(
                username=user_create.username,
                password="some password create",
                email="some email create",
            )
        except Exception as e:
            assert str(e) == f"username: {user_create.username} already use"
        finally:
            UserModel.delete_model(user_create)

    def test_error_create_same_user_with_same_email(self):
        user_create = UserModel.add_model(
            username="create user name second",
            email="createemailsecontest@gmail.come",
            password="create password",
        )
        try:
            same_user_two = UserModel.add_model(
                username="another user name test",
                password="some password create",
                email=user_create.email,
            )
        except Exception as e:
            assert str(e) == f"email: {user_create.email} already use"
        finally:
            UserModel.delete_model(user_create)
