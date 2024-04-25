"""_summary_
"""

from .user_image_data import UserImageData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from app.model_base_service import db, ModelBaseService


class UserImageModel(UserImageData, ModelBaseService["UserImageModel"], db.Model):
    __tablename__ = "user_image"
    id = mapped_column("image_id", String(36), primary_key=True)
    image_url = mapped_column("image_url", String(50))
    user_id = mapped_column("user_id", String, ForeignKey("user.user_id"))

    def _clean_up_all_model(self):
        return self.session.query(UserImageModel).all()
