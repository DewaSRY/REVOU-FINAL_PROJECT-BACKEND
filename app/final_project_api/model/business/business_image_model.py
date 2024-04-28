"""_summary_
"""

from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey

from app.model_base_service import db, ModelBaseService

from .business_image_data import BusinessImageData


class BusinessImageModel(
    BusinessImageData, ModelBaseService["BusinessImageModel"], db.Model
):
    __tablename__ = "business_images"
    public_id = mapped_column("public_id", String(36), primary_key=True)
    secure_url = mapped_column("secure_url", String(50))
    business_id = mapped_column(
        "business_id", String(36), ForeignKey("business.business_id")
    )

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
    def add_model(
        cls, secure_url: str, public_id: str, business_id: str
    ) -> "BusinessImageModel":
        from .business_model import BusinessModel

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
