# """_summary_
# """

# from tests.mock_database_connection import MockDatabaseConnection
# from app.final_project_api.model.user import UserModel
# from app.final_project_api.model.business import (
#     BusinessDate,
#     BusinessImageData,
#     BusinessImageModel,
#     BusinessModel,
#     BusinessTypeData,
#     BusinessTypeModel,
# )
# from pprint import pprint


# class TestBusinessModel(MockDatabaseConnection):

#     def setup_class(self):
#         super().setup_class(self)
#         self.user_test = UserModel.add_model(
#             username="business name",
#             email="business email",
#             password="business password",
#         )
#         self.business_type_test = BusinessTypeModel.add_model(
#             BusinessTypeModel(name="some name")
#         )

#     def teardown_class(self):
#         super().teardown_class(self)
#         UserModel.clean_all_model()
#         BusinessTypeModel.delete_model(self.business_type_test)

#     def test_create_business_first(self):
#         businessCreate = BusinessModel.add_model(
#             BusinessModel(
#                 user_id=self.user_test.id,
#                 business_name="some business name",
#                 business_type_name=self.business_type_test.name,
#             )
#         )
#         assert businessCreate.user_id == self.user_test.id
#         assert businessCreate.business_types == self.business_type_test.name
#         assert businessCreate.business_type_id == self.business_type_test.id

#     def test_create_business_image(self):
#         businessCreate = BusinessModel.add_model(
#             BusinessModel(
#                 user_id=self.user_test.id,
#                 business_name="some business name",
#                 business_type_name=self.business_type_test.name,
#             )
#         )
#         image_one, image_two, image_three = BusinessImageModel.add_all_model(
#             [
#                 BusinessImageModel(image_url="some url", business_id=businessCreate.id),
#                 BusinessImageModel(
#                     image_url="some url two", business_id=businessCreate.id
#                 ),
#                 BusinessImageModel(
#                     image_url="some url three", business_id=businessCreate.id
#                 ),
#             ]
#         )
#         user_image_one, user_image_two, user_image_three = (
#             businessCreate.business_images
#         )
#         assert image_one.image_url == user_image_one
#         assert image_two.image_url == user_image_two
#         assert image_three.image_url == user_image_three
