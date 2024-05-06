# """_summary_
# """

# # from pprint import pprint
# # from unittest import skip
# from uuid import uuid4

# from tests.mock_database_connection import MockDatabaseConnection

# from app.final_project_api.user_module.model import UserModel

# from app.final_project_api.business_module.model import BusinessModel
# from app.final_project_api.business_module.image_model import BusinessImageModel
# from app.final_project_api.business_module.type_model import BusinessTypeModel


# class TestCreateBusinessImage(MockDatabaseConnection):

#     def setup_class(self):
#         super().setup_class(self)
#         UserModel.clean_all()
#         BusinessTypeModel.clean_all()
#         BusinessModel.clean_all()
#         self.business_name = "some name test"
#         self.business_description = "some description "

#     def tearDown(self) -> None:
#         UserModel.clean_all()
#         BusinessTypeModel.clean_all()
#         BusinessModel.clean_all()
#         BusinessImageModel.clean_all()

#     def setUp(self) -> None:
#         super().setUp()
#         self.user_create = UserModel.add_model(
#             email="some@mail.com", password="some password", username="some user name"
#         )
#         self.business_type = BusinessTypeModel.add_model(name="some type")

#     def test_create_business_image(self):
#         first_url = "firstUrl"
#         second_url = "secondUrl"
#         create_business = BusinessModel.add_model(
#             business_name=self.business_name,
#             business_type_name=self.business_type.name,
#             user_id=self.user_create.id,
#             description=self.business_description,
#         )
#         first_profile_url = create_business.profile_url
#         BusinessImageModel.add_model(
#             public_id=str(uuid4()), business_id=create_business.id, secure_url=first_url
#         )
#         profile_url_after_first_image = create_business.profile_url
#         BusinessImageModel.add_model(
#             public_id=str(uuid4()),
#             business_id=create_business.id,
#             secure_url=second_url,
#         )
#         profile_url_after_second_image = create_business.profile_url
#         assert first_profile_url == ""
#         assert profile_url_after_first_image == first_url
#         assert profile_url_after_second_image == first_url
