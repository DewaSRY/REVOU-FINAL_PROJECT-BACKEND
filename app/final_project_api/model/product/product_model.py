"""_summary_
"""

from .product_data import ProductData
from sqlalchemy.orm import mapped_column
from sqlalchemy import Float, String
from app.model_base_service import db, ModelBaseService


class ProductModel(ProductData, ModelBaseService["ProductModel"], db.Model):
    __tablename__ = "product"
    product_id = mapped_column("product_id", String(36), primary_key=True)
    product_name = mapped_column("product_name", String(50))
    product_price = mapped_column("product_price", Float(10.2))

    @property
    def product_images(self):
        from .product_image_model import ProductImageModel

        imageList: list[ProductImageModel] = (
            self.session.query(ProductImageModel)
            .filter(ProductImageModel.product_id == self.id)
            .all()
        )
        if len(imageList) == 0:
            return []
        return [img.image_url for img in imageList]
