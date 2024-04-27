"""_summary_
"""

from .product_data import ProductData
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, Float
from app.model_base_service import db, ModelBaseService
from typing import Union


class ProductModel(ProductData, ModelBaseService["ProductModel"], db.Model):
    __tablename__ = "product"
    id = mapped_column("product_id", String(36), primary_key=True)
    product_name = mapped_column("product_name", String(50))
    product_price = mapped_column("product_price", Float(10.2))
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    update_at = mapped_column(
        "updated_at", DateTime(timezone=True), onupdate=datetime.now
    )
    user_id = mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    business_id = mapped_column(
        "business_id", String(36), ForeignKey("business.business_id")
    )

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

    def _set_user_id(self):
        from app.final_project_api.model.business import BusinessModel

        self.user_id = (
            self.session.query(BusinessModel)
            .filter(BusinessModel.id == self.business_id)
            .first()
            .user_id
        )

    @classmethod
    def get_by_user_id(cls, user_id: str) -> list["ProductModel"]:
        return (
            cls.session.query(ProductModel)
            .filter(ProductModel.user_id == user_id)
            .all()
        )

    @classmethod
    def get_by_business_id(cls, business_id: str) -> list["ProductModel"]:
        return (
            cls.session.query(ProductModel)
            .filter(ProductModel.business_id == business_id)
            .all()
        )
