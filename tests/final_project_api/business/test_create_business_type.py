# """_summary_
# """

# from tests.mock_database_connection import MockDatabaseConnection
# from app.final_project_api.business_module.type_model import BusinessTypeModel
# from pprint import pprint
# from unittest import skip


# class TestCreateBusinessType(MockDatabaseConnection):

#     def setup_class(self):
#         super().setup_class(self)
#         self.type_name_one = "type_name_one"

#     def setUp(self) -> None:
#         BusinessTypeModel.clean_all_model()

#     def tearDown(self) -> None:
#         BusinessTypeModel.clean_all_model()

#     # @skip("just skip")
#     def test_create(self):
#         type_create = BusinessTypeModel.add_model(name=self.type_name_one)

#         assert type_create.name == self.type_name_one
#         assert type_create.id == 1
