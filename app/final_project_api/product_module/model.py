"""_summary_
"""

from typing import Self, Union
from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, Integer, ForeignKey, Float, Boolean, desc

from .data import ProductData, ProductUpdateData
from app.util import QueryData
from app.model_base_service import db, ModelBaseService


class ProductModel(ProductData, ModelBaseService, db.Model):
    __tablename__ = "product"
    id = mapped_column("product_id", String(36), primary_key=True)
    product_name = mapped_column("product_name", String(50))
    description = mapped_column("description", String(50))
    profile_url = mapped_column("profile_url", String(50))
    product_price = mapped_column("product_price", Float(10.2))
    is_delete = mapped_column("is_delete", Boolean, default=False)

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
        from app.final_project_api.business_module.model import BusinessModel

        model: BusinessModel = BusinessModel.get_by_id(model_id=self.business_id)
        return model.business_name

    @property
    def username(self):
        from app.final_project_api.user_module.model import UserModel

        model: UserModel = UserModel.get_by_id(model_id=self.user_id)
        return model.username

    @property
    def product_images(self):
        from .image_model import ProductImageModel as PM

        imageList: list[PM] = PM.get_image_by_product_id(product_id=self.id)
        if len(imageList) == 0:
            return []
        return imageList

    @classmethod
    def total_row(cls):
        return cls.session.query(ProductModel).count()

    @classmethod
    def delete_model_by_id(cls, model_id: str):
        productModel: ProductModel = ProductModel.get_by_id(model_id=model_id)
        productModel.is_delete = True
        cls.session.add(productModel)
        cls.session.commit()
        return productModel

    @classmethod
    def update_with_update_data(cls, product_id: str, product_data: ProductUpdateData):
        productModel: Self = ProductModel.get_by_id(model_id=product_id)
        productModel._update(
            product_name=product_data.product_name,
            description=product_data.description,
            product_price=product_data.product_price,
        )
        cls.session.add(productModel)
        cls.session.commit()
        return productModel

    @classmethod
    def get_by_id(cls, model_id: str):
        return (
            cls.session.query(ProductModel).filter(ProductModel.id == model_id).first()
        )

    @classmethod
    def get_all_public(cls, query_data: QueryData = QueryData()):
        queryPointer = cls.session.query(ProductModel)
        if len(query_data.search) != 0:
            return (
                queryPointer.filter(ProductModel.is_delete == False)
                .filter(ProductModel.product_name.like(query_data.getSearch()))
                .order_by(desc(ProductModel.create_at))
                .all()
            )
        offset = (query_data.page - 1) * query_data.limit
        return (
            queryPointer.filter(ProductModel.is_delete == False)
            .order_by(desc(ProductModel.create_at))
            .limit(query_data.limit)
            .offset(offset)
            .all()
        )

    @classmethod
    def add_model(
        cls, business_id: str, product_name: str, product_price: float, description: str
    ) -> "ProductModel":
        model = ProductModel(
            business_id=business_id,
            product_name=product_name,
            product_price=product_price,
            description=description,
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

    def _set_user_id(self):
        from app.final_project_api.business_module.model import BusinessModel as BM

        model: BM = BM.get_by_id(model_id=self.business_id)
        self.user_id = model.user_id

    def _get_all(self):
        return self.session.query(ProductModel).all()

    def _get_by_id(self, model_id: str):
        return self.session.query(ProductModel).filter(ProductModel.id == model_id)

    def _update(
        self,
        product_name: str = "",
        product_price: float = 0,
        description: str = "",
    ):
        if product_price != self.product_price:
            self.product_price = product_price
        if len(product_name) != 0:
            self.product_name = product_name
        if len(description) != 0:
            self.description = description
