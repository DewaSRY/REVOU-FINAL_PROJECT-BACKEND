"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection

from app.final_project_api.user_module.model import UserModel
from app.final_project_api.business_module.model import BusinessModel
from app.final_project_api.business_module.type_model import BusinessTypeModel
from app.final_project_api.product_module.model import ProductModel
from app.final_project_api.product_module.image_model import ProductImageModel
from pprint import pprint
from unittest import skip
from uuid import uuid4


class TestUpdateImage(MockDatabaseConnection):

    def setup_class(self):
        super().setup_class(self)
        UserModel.clean_all()
        BusinessModel.clean_all()
        self.product_name = "some product name"
        self.product_price = 1_000
        self.product_description = "some description"

    def setUp(self) -> None:
        self.user_create = UserModel.add_model(
            username="product user name",
            email="product@email.com",
            password="some password",
        )
        self.business_type = BusinessTypeModel.add_model(name="business product type")
        self.business = BusinessModel.add_model(
            user_id=self.user_create.id,
            business_name="some business name",
            business_type_name=self.business_type.name,
            description="some business description ",
        )
        self.create_product = ProductModel.add_model(
            business_id=self.business.id,
            product_name=self.product_name,
            product_price=self.product_price,
            description=self.product_description,
        )

    def tearDown(self) -> None:
        UserModel.clean_all()
        BusinessTypeModel.clean_all()
        BusinessModel.clean_all()
        ProductImageModel.clean_all()
        ProductModel.clean_all()

    def test_create_product_image(self):
        first_url = "first ulr"
        second_url = "second ulr"

        default_profile_url = self.create_product.profile_url
        ProductImageModel.add_model(
            public_id=str(uuid4()),
            secure_url=first_url,
            product_id=self.create_product.id,
        )
        profile_url_after_first_image = self.create_product.profile_url
        ProductImageModel.add_model(
            public_id=str(uuid4()),
            secure_url=second_url,
            product_id=self.create_product.id,
        )
        profile_url_after_second_image = self.create_product.profile_url
        assert default_profile_url == ""
        assert profile_url_after_first_image == first_url
        assert profile_url_after_second_image == first_url

    # @skip("just skip")
