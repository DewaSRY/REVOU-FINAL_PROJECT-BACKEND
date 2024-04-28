"""_summary_
"""

from .product_image_data import ProductImageData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.model_base_service import db, ModelBaseService


class ProductImageModel(
    ProductImageData, ModelBaseService["ProductImageModel"], db.Model
):
    __tablename__ = "product_images"
    public_id = mapped_column("image_id", String(36), primary_key=True)
    secure_url = mapped_column("secure_url", String(50))
    product_id = mapped_column(
        "product_id", String(36), ForeignKey("product.product_id")
    )

    def _get_all_model(self):
        return self.session.query(ProductImageModel).all()

    def _get_model_by_id(self, model_id: str) -> "ProductImageModel":
        return (
            self.session.query(ProductImageModel)
            .filter(ProductImageModel.id == model_id)
            .first()
        )

    @classmethod
    def get_image_by_product_id(cls, product_id: str) -> list["ProductImageModel"]:
        return (
            cls.session.query(ProductImageModel)
            .filter(ProductImageModel.product_id == product_id)
            .all()
        )

    @classmethod
    def add_model(
        cls, secure_url: str, public_id: str, product_id: str
    ) -> "ProductImageModel":
        from .product_model import ProductModel

        productModel: ProductModel = ProductModel.get_model_by_id(model_id=product_id)
        if bool(productModel.profile_url) != True:
            productModel.profile_url = secure_url

        model = ProductImageModel(
            public_id=public_id, secure_url=secure_url, product_id=product_id
        )

        cls.session.add(model)
        cls.session.commit()
        return model
