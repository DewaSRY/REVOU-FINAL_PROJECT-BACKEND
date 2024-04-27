"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from app.final_project_api.model.business import BusinessTypeModel
from app.data_store_service import DataStore
from pprint import pprint


class TestCreateBusinessType(MockDatabaseConnection):

    def setup_class(self):
        super().setup_class(self)
        self.type_name_one = "type_name_one"

    def setUp(self) -> None:
        BusinessTypeModel.clean_all_model()

    def tearDown(self) -> None:
        BusinessTypeModel.clean_all_model()

    def test_create(self):
        type_create = BusinessTypeModel.add_model(name=self.type_name_one)

        assert type_create.name == self.type_name_one
        assert type_create.id == 1
        assert self.type_name_one in DataStore.BUSINESS_TYP_LIST
        assert type_create.name in DataStore.BUSINESS_TYP_LIST
