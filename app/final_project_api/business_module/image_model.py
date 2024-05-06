"""_summary_
"""

from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime

from app.model_base_service import db, ModelBaseService

from .data import BusinessImageData
from .model import BusinessModel


class BusinessImageModel(
    BusinessImageData, ModelBaseService["BusinessImageModel"], db.Model
):
    __tablename__ = "business_images"
    id = mapped_column("id", String(36), primary_key=True)
    public_id = mapped_column("public_id", String(36))
    secure_url = mapped_column("secure_url", String(50))
    business_id = mapped_column(
        "business_id", String(36), ForeignKey("business.business_id")
    )
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )

    @property
    def business_name(self):
        bModel: BusinessModel = BusinessModel.get_model_by_id(model_id=self.business_id)
        return bModel.business_name

    def _get_all_model(self):
        return self.session.query(BusinessImageModel).all()

    def _get_model_by_id(self, model_id: str) -> "BusinessImageModel":
        return (
            self.session.query(BusinessImageModel)
            .filter(BusinessImageModel.id == model_id)
            .first()
        )

    @classmethod
    def get_image_by_business_id(cls, business_id: str) -> list["BusinessImageModel"]:
        return (
            cls.session.query(BusinessImageModel)
            .filter(BusinessImageModel.business_id == business_id)
            .all()
        )

    @classmethod
    def put_as_profile(cls, image_id: str) -> BusinessModel:

        imageMode: BusinessImageModel = BusinessImageModel.get_model_by_id(
            model_id=image_id
        )
        businessModel: BusinessModel = BusinessModel.get_model_by_id(
            model_id=imageMode.business_id
        )
        businessModel.profile_url = imageMode.secure_url
        cls.session.add(businessModel)
        cls.session.commit()
        return businessModel

    @classmethod
    def add_model(
        cls, secure_url: str, public_id: str, business_id: str
    ) -> "BusinessImageModel":

        businessModel: BusinessModel = BusinessModel.get_model_by_id(
            model_id=business_id
        )
        if bool(businessModel.profile_url) != True:
            businessModel.profile_url = secure_url

        model = BusinessImageModel(
            public_id=public_id, secure_url=secure_url, business_id=business_id
        )

        cls.session.add(model)
        cls.session.commit()
        return model
