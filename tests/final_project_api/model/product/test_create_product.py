"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection

from app.final_project_api.model.user import UserModel
from app.final_project_api.model.business import BusinessModel, BusinessTypeModel
from app.final_project_api.model.product import ProductModel
from pprint import pprint


class TestCreateProduct(MockDatabaseConnection):

    def setup_class(self):
        super().setup_class(self)
        self.product_name = "some product name"
        self.product_price = 1_000

    def setUp(self) -> None:
        self.user_create = UserModel.add_model(
            username="business user name",
            email="business@email.com",
            password="some password",
        )
        self.business_type = BusinessTypeModel.add_model(name="business type")
        self.business = BusinessModel.add_model(
            user_id=self.user_create.id,
            business_name="some business name",
            business_type_name=self.business_type.name,
        )

    def tearDown(self) -> None:
        UserModel.clean_all_model()
        BusinessTypeModel.clean_all_model()
        BusinessModel.clean_all_model()

    def test_create_product(self):
        create_product = ProductModel.add_model(
            business_id=self.business.id,
            product_name=self.product_name,
            product_price=self.product_price,
        )
        pprint(create_product, indent=2)
