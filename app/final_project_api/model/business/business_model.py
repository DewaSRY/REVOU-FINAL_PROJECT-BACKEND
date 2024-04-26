"""_summary_
"""

from .business_data import BusinessDate
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, String, Integer
from app.model_base_service import db, ModelBaseService


class BusinessModel(BusinessDate, ModelBaseService["BusinessModel"], db.Model):
    __tablename__ = "business"
    id = mapped_column("business_id", String(36), primary_key=True)
    user_id = mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    business_name = mapped_column("name", String(50))

    @property
    def business_images(self):
        from .business_image_model import BusinessImageModel

        imagesList = (
            self.session.query(BusinessImageModel)
            .filter(BusinessImageModel.business_id == self.id)
            .all()
        )
        if len(imagesList) == 0:
            return []
        return [img.image_url for img in imagesList]

    @property
    def business_types(self):
        from .business_type_model import BusinessTypeModel

        return (
            self.session.query(BusinessTypeModel)
            .filter(BusinessTypeModel.id == self.business_type_id)
            .first()
            .name
        )

    def _set_match_business_type(self, business_type_name: str):
        from .business_type_model import BusinessTypeModel

        businessType = (
            self.session.query(BusinessTypeModel)
            .filter(BusinessTypeModel.name.like(business_type_name))
            .first()
        )
        self.business_type_id = businessType.id

    def _clean_up_all_model(self):
        return self.session.query(BusinessModel).all()
