"""_summary_
"""

from app.model_base_service.db import Base
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
    profile_url = mapped_column("profile_url", String(50))
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
    def business_name(self):
        from app.final_project_api.model.business import BusinessModel

        model: BusinessModel = BusinessModel.get_model_by_id(model_id=self.business_id)
        return model.business_name

    @property
    def username(self):
        from app.final_project_api.model.user import UserModel

        model: UserModel = UserModel.get_model_by_id(model_id=self.user_id)
        return model.username

    @property
    def product_images(self):
        from .product_image_model import ProductImageModel as PM

        imageList: list[PM] = PM.get_image_by_product_id(product_id=self.id)
        if len(imageList) == 0:
            return []
        return [img.secure_url for img in imageList]

    def _set_user_id(self):
        from app.final_project_api.model.business import BusinessModel as BM

        model: BM = BM.get_model_by_id(model_id=self.business_id)
        self.user_id = model.user_id

    def _get_all_model(self):
        return self.session.query(ProductModel).all()

    def _get_model_by_id(self, model_id: str) -> "ProductModel":
        return (
            self.session.query(ProductModel).filter(ProductModel.id == model_id).first()
        )

    @classmethod
    def add_model(
        cls, business_id: str, product_name: str, product_price: float
    ) -> "ProductModel":
        model = ProductModel(
            business_id=business_id,
            product_name=product_name,
            product_price=product_price,
        )
        cls.session.add(model)
        cls.session.commit()
        return model

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
