"""_summary_
"""

from .model import UserModel
from .data import UserImageData

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey, DateTime
from app.model_base_service import db, ModelBaseService


class UserImageModel(UserImageData, ModelBaseService["UserImageModel"], db.Model):
    __tablename__ = "user_image"
    id = mapped_column("id", String(36), primary_key=True)
    public_id = mapped_column("public_id", String(36))
    secure_url = mapped_column("secure_url", String(50))
    user_id = mapped_column("user_id", String, ForeignKey("user.user_id"))
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )

    @property
    def username(self):
        userModel: UserModel = UserModel.get_model_by_id(model_id=self.user_id)
        return userModel.username

    @classmethod
    def put_as_profile(cls, image_id: str) -> "UserModel":

        imageMode = UserImageModel.get_model_by_id(model_id=image_id)
        userModel: UserModel = UserModel.get_model_by_id(model_id=imageMode.user_id)
        userModel.profile_url = imageMode.secure_url
        cls.session.add(userModel)
        cls.session.commit()
        return userModel

    @classmethod
    def delete_model_by_id(cls, model_id: str):
        imageModel = UserImageModel.get_model_by_id(model_id=model_id)
        userModel: UserModel = UserModel.get_model_by_id(model_id=imageModel.user_id)
        if imageModel.secure_url == userModel.profile_url:
            userModel.profile_url = ""
            cls.session.add(userModel)

        cls.session.delete(imageModel)
        cls.session.commit()
        return imageModel

    @classmethod
    def get_model_by_id(cls, model_id: str) -> "UserImageModel":
        return (
            cls.session.query(UserImageModel)
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

        userModel: UserModel = UserModel.get_model_by_id(model_id=user_id)
        if bool(userModel.profile_url) != True:
            userModel.profile_url = secure_url

        model = UserImageModel(
            public_id=public_id, secure_url=secure_url, user_id=user_id
        )

        cls.session.add(model)
        cls.session.commit()
        return model

    def _get_all_model(self):
        return self.session.query(UserImageModel).all()
