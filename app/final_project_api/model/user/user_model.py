"""_summary_
Returns:
    _type_: _description_
"""

from sqlalchemy.sql import func
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from sqlalchemy import String, DateTime
from sqlalchemy.orm import (
    mapped_column,
)
from app.model_base_service import db, ModelBaseService
from app.model_base_service.model_base import ModelBase

from .user_data import UserData
from typing import Union


class UserModel(UserData, ModelBaseService[UserData], db.Model):
    __tablename__ = "user"

    id = mapped_column("user_id", String(36), primary_key=True)
    username = mapped_column("username", String(50), unique=True, nullable=False)
    email = mapped_column("email", String(50), unique=True)
    password = mapped_column("password_hash", String(200))
    created_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    updated_at = mapped_column(
        "updated_at", DateTime(timezone=True), onupdate=datetime.now
    )

    def _set_password(self, password: str) -> None:
        self.password = pbkdf2_sha256.hash(password)

    def _delete(self):
        self.session.delete(self)

    def match_password(self, receive_password: str) -> bool:
        return pbkdf2_sha256.verify(secret=receive_password, hash=self.password)

    def _clean_up_all_model(self) -> list[ModelBase]:
        return self.session.query(UserModel).all()

    def _update(self, username: str = None, email: str = None, password: str = None):
        if username != None:
            self.username = username
        if email != None:
            self.email = email
        if password != None:
            self._set_password(password)
        self.update_at = datetime.now()

    @classmethod
    def get_by_email_or_username(
        cls, username: str = None, email: str = None
    ) -> Union["UserModel", None]:
        if username != None:
            cls.session.query(UserModel).filter(UserModel.username == username).first()
        if email != None:
            cls.session.query(UserModel).filter(UserModel.email == email).first()
        return None
