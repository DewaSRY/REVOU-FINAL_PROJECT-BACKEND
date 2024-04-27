"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection

from app.final_project_api.model.user import UserModel
from app.final_project_api.model.business import (
    BusinessTypeModel,
    BusinessModel,
)
from pprint import pprint


class TestCreateBusiness(MockDatabaseConnection):

    def setup_class(self):
        super().setup_class(self)
        UserModel.clean_all_model()
        BusinessTypeModel.clean_all_model()
        BusinessModel.clean_all_model()
        self.business_name = "some name"

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        BusinessTypeModel.clean_all_model()
        BusinessModel.clean_all_model()

    def setUp(self) -> None:
        super().setUp()
        self.user_create = UserModel.add_model(
            email="some@mail.com", password="some password", username="some user name"
        )
        self.business_type = BusinessTypeModel.add_model(name="some type")

    def test_create_business(self):
        create_business = BusinessModel.add_model(
            business_name=self.business_name,
            business_type_name=self.business_type.name,
            user_id=self.user_create.id,
        )
        assert create_business.user_id == self.user_create.id
        assert create_business.business_name == self.business_name
        assert create_business.business_types == self.business_type.name
