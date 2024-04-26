# """_summary_
# """

# from tests.mock_database_connection import MockDatabaseConnection
# from app.final_project_api.model.product import (
#     ProductImageModel,
#     ProductImageData,
#     ProductData,
#     ProductModel,
# )
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


# class TestProductModel(MockDatabaseConnection):

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
#         self.business_test = BusinessModel.add_model(
#             BusinessModel(
#                 user_id=self.user_test.id,
#                 business_name="some business name",
#                 business_type_name=self.business_type_test.name,
#             )
#         )

#     def teardown_class(self):
#         super().teardown_class(self)
#         UserModel.clean_all_model()
#         BusinessTypeModel.delete_model(self.business_type_test)
#         BusinessModel.clean_all_model()

#     def test_create_product_first(self):
#         productName = "product name"
#         productPrice = 10_000
#         productCreate = ProductModel.add_model(
#             ProductModel(
#                 business_id=self.business_test.id,
#                 product_name=productName,
#                 product_price=productPrice,
#             )
#         )
#         # pprint(productCreate, indent=2)
#         assert productCreate.user_id == self.business_test.user_id
#         assert productCreate.product_name == productName
#         assert productCreate.product_price == productPrice
#         assert productCreate.business_id == self.business_test.id

#     def test_create_business_image(self):

#         productCreate = ProductModel.add_model(
#             ProductModel(
#                 business_id=self.business_test.id,
#                 product_name="some name",
#                 product_price=100_00,
#             )
#         )
#         image_one, image_two, image_three = ProductImageModel.add_all_model(
#             [
#                 ProductImageModel(image_url="some url", product_id=productCreate.id),
#                 ProductImageModel(
#                     image_url="some url two", product_id=productCreate.id
#                 ),
#                 ProductImageModel(
#                     image_url="some url three", product_id=productCreate.id
#                 ),
#             ]
#         )
#         user_image_one, user_image_two, user_image_three = productCreate.product_images
#         assert image_one.image_url == user_image_one
#         assert image_two.image_url == user_image_two
#         assert image_three.image_url == user_image_three
