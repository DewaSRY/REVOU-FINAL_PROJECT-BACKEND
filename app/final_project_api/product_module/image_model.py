"""_summary_
"""

from typing import Self
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func

from .model import ProductModel
from .data import ProductImageData

from app.message_service import MessageService
from app.model_base_service import db, ModelBaseService


class ProductImageModel(ProductImageData, ModelBaseService, db.Model):
    __tablename__ = "product_images"
    id = mapped_column("id", String(36), primary_key=True)
    public_id = mapped_column("public_id", String(36))
    secure_url = mapped_column("secure_url", String(50))
    product_id = mapped_column(
        "product_id", String(36), ForeignKey("product.product_id")
    )
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )

    @property
    def product_name(self):

        productModel: ProductModel = ProductModel.get_by_id(model_id=self.product_id)
        return productModel.product_name

    @classmethod
    def put_as_profile(cls, image_id: str) -> "ProductModel":

        imageMode: Self = ProductImageModel.get_by_id(model_id=image_id)
        productModel: ProductModel = ProductModel.get_by_id(
            model_id=imageMode.product_id
        )
        productModel.profile_url = imageMode.secure_url
        cls.session.add(productModel)
        cls.session.commit()
        return productModel

    @classmethod
    def delete_model_by_id(cls, model_id: str):

        imageModel = ProductImageModel.get_by_id(model_id=model_id)
        productModel: ProductModel = ProductModel.get_by_id(model_id=imageModel.user_id)
        if imageModel.secure_url == productModel.profile_url:
            productModel.profile_url = ""
            cls.session.add(productModel)

        cls.session.delete(imageModel)
        cls.session.commit()
        return imageModel

    @classmethod
    def get_by_id(cls, model_id: str):
        return (
            cls.session.query(ProductImageModel)
            .filter(ProductImageModel.id == model_id)
            .first()
        )

    @classmethod
    def get_image_by_product_id(cls, product_id: str) -> list[Self]:
        return (
            cls.session.query(ProductImageModel)
            .filter(ProductImageModel.product_id == product_id)
            .all()
        )

    @classmethod
    def add_model(
        cls, secure_url: str, public_id: str, product_id: str
    ) -> "ProductImageModel":

        productModel: ProductModel = ProductModel.get_by_id(model_id=product_id)
        if bool(productModel) == False:
            message = MessageService.get_message("product_not_found").format(product_id)
            raise Exception(message)

        if bool(productModel.profile_url) != True:
            productModel.profile_url = secure_url

        model = ProductImageModel(
            public_id=public_id, secure_url=secure_url, product_id=product_id
        )

        cls.session.add(model)
        cls.session.commit()
        return model

    def _get_all(self):
        return self.session.query(ProductImageModel).all()
