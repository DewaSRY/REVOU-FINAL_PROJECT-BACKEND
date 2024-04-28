"""_summary_
"""

from .user_image_data import UserImageData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from app.model_base_service import db, ModelBaseService


class UserImageModel(UserImageData, ModelBaseService["UserImageModel"], db.Model):
    __tablename__ = "user_image"
    public_id = mapped_column("public_id", String(36), primary_key=True)
    secure_url = mapped_column("secure_url", String(50))
    user_id = mapped_column("user_id", String, ForeignKey("user.user_id"))

    def _get_all_model(self):
        return self.session.query(UserImageModel).all()

    def _get_model_by_id(self, model_id: str) -> "UserImageModel":
        return (
            self.session.query(UserImageModel)
            .filter(UserImageModel.id == model_id)
            .first()
        )

    @classmethod
    def get_image_by_user_id(cls, user_id: str) -> list["UserImageModel"]:
        return (
            cls.session.query(UserImageModel)
            .filter(UserImageModel.user_id == user_id)
            .all()
        )

    @classmethod
    def add_model(
        cls, secure_url: str, public_id: str, user_id: str
    ) -> "UserImageModel":
        from .user_model import UserModel

        userModel: UserModel = UserModel.get_model_by_id(model_id=user_id)
        if bool(userModel.profile_url) != True:
            userModel.profile_url = secure_url

        model = UserImageModel(
            public_id=public_id, secure_url=secure_url, user_id=user_id
        )

        cls.session.add(model)
        cls.session.commit()
        return model
