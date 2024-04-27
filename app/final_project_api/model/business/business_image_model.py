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
    id = mapped_column("id", String(36), primary_key=True)
    image_url = mapped_column("image_url", String(50))
    business_id = mapped_column(
        "business_id", String(36), ForeignKey("business.business_id")
    )
