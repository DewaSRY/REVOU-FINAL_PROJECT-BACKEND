"""_summary_
Returns:
    _type_: _description_
"""

from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import (
    mapped_column,
)
from app.model_base_service import db, ModelBaseService
from app.model_base_service.db import Base
from app.model_base_service.model_base import ModelBase

from .user_data import UserData
from typing import Union
from pprint import pprint


class UserModel(UserData, ModelBaseService[UserData], db.Model):
    __tablename__ = "user"

    id = mapped_column("user_id", String(36), primary_key=True)
    username = mapped_column("username", String(50), unique=True, nullable=False)

    phone_number = mapped_column(
        "phone_number", String(50), unique=True, nullable=False
    )
    address = mapped_column("address", String(50), unique=True, nullable=False)
    occupation = mapped_column("occupation", String(50), unique=True, nullable=False)
    description = mapped_column("description", Text, unique=True, nullable=False)

    email = mapped_column("email", String(50), unique=True)
    profile_url = mapped_column("profile_url", String(50), server_default="")
    password = mapped_column("password_hash", String(200))
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    update_at = mapped_column(
        "updated_at", DateTime(timezone=True), onupdate=datetime.now
    )
    user_type_id = mapped_column("user_type_id", Integer, ForeignKey("user_type.id"))

    @property
    def business_amount(self):
        from app.final_project_api.model.business import BusinessModel as BM

        return len(BM.get_by_user_id(self.id))

    @property
    def product_amount(self):
        from app.final_project_api.model.product import ProductModel as PM

        return len(PM.get_by_user_id(self.id))

    @property
    def business(self):
        from app.final_project_api.model.business import BusinessModel

        return BusinessModel.get_by_user_id(self.id)

    @property
    def product(self):
        from app.final_project_api.model.product import ProductModel

        return ProductModel.get_by_user_id(self.id)

    @property
    def user_type(self):
        from .user_type_model import UserTypeModel
        from app.data_store_service import DataStore

        type = UserTypeModel.get_model_by_id(self.user_type_id)
        if type == None:
            raise Exception(
                f"please use register type :{str(DataStore.USER_TYPE_LIST)} "
            )
        return type.name

    @property
    def user_images(self):
        from .user_image_model import UserImageModel

        userImages = UserImageModel.get_image_by_user_id(self.id)
        if len(userImages) == 0:
            return []

        return [img.secure_url for img in userImages]

    def _get_model_by_id(self, model_id: str) -> Union["UserModel", None]:
        return self.session.query(UserModel).filter(UserModel.id == model_id).first()

    def _get_all_model(self) -> list[ModelBase]:
        return self.session.query(UserModel).all()

    def _update(
        self,
        username: str = None,
        phone_number: str = None,
        address: str = None,
        occupation: str = None,
        description: str = None,
        email: str = None,
        password: str = None,
    ):
        if username != None:
            self.username = username
        if phone_number != None:
            self.phone_number = phone_number
        if address != None:
            self.address = address
        if occupation != None:
            self.occupation = occupation
        if description != None:
            self.description = description
        if email != None:
            self.email = email
        if password != None:
            self._set_password(password)
        self.update_at = datetime.now()

    @classmethod
    def update_with_id(
        cls,
        user_id: str,
        username: str = None,
        phone_number: str = None,
        address: str = None,
        occupation: str = None,
        description: str = None,
        email: str = None,
        password: str = None,
    ):
        userModel: UserModel = UserModel.get_model_by_id(model_id=user_id)
        userModel._update(
            username=username,
            address=address,
            description=description,
            email=email,
            occupation=occupation,
            password=password,
            phone_number=phone_number,
        )
        cls.session.add(userModel)
        cls.session.commit()
        return userModel

    @classmethod
    def get_by_email_or_username(
        cls, username: str = "", email: str = ""
    ) -> Union["UserModel", None]:

        query_pointer = cls.session.query(UserModel)
        by_username = query_pointer.filter(UserModel.username.like(username)).first()
        by_email = query_pointer.filter(UserModel.email.like(email)).first()

        if bool(by_username) == True:
            return by_username
        if bool(by_email) == True:
            return by_email

        return None

    @classmethod
    def add_model(cls, username: str, email: str, password) -> UserData:
        model = UserModel(username=username, email=email, password=password)
        model_pointer = cls.session.query(UserModel)
        if len(model_pointer.all()) != 0:
            if model_pointer.filter(UserModel.username == (username)).first() != None:
                raise Exception(f"username: '{username}' already use")
            elif model_pointer.filter(UserModel.email == (email)).first() != None:
                raise Exception(f"email: '{email}' already use")
        cls.session.add(model)
        cls.session.commit()
        return model
