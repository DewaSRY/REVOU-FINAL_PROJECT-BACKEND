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
from app.model_base_service.model_base import ModelBase
from .data import UserData, UserUpdateData
from typing import Union
from pprint import pprint


class UserModel(UserData, ModelBaseService, db.Model):
    __tablename__ = "user"
    id = mapped_column("user_id", String(36), primary_key=True)
    username = mapped_column("username", String(50), unique=True, nullable=False)
    phone_number = mapped_column("phone_number", String(20))
    address = mapped_column("address", String(50))
    occupation = mapped_column("occupation", String(50))
    description = mapped_column("description", Text)

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
        from app.final_project_api.business_module.model import BusinessModel as BM

        return len(BM.get_by_user_id(self.id))

    @property
    def product_amount(self):
        from app.final_project_api.product_module.model import ProductModel as PM

        return len(PM.get_by_user_id(self.id))

    @property
    def business(self):
        from app.final_project_api.business_module.model import BusinessModel

        return BusinessModel.get_by_user_id(self.id)

    @property
    def product(self):
        from app.final_project_api.product_module.model import ProductModel

        return ProductModel.get_by_user_id(self.id)

    @property
    def user_type(self):
        from .type_model import UserTypeModel

        type = UserTypeModel.get_by_id(self.user_type_id)
        if type == None:
            raise Exception(f"user type with id {self.user_type_id }  not found")
        return type.name

    @property
    def images(self):
        from .image_model import UserImageModel

        userImages = UserImageModel.get_image_by_user_id(self.id)
        if len(userImages) == 0:
            return []

        return userImages

    @classmethod
    def update_with_update_data(cls, user_id: str, update_data: UserUpdateData):
        userModel: UserModel = UserModel.get_by_id(model_id=user_id)
        userModel._update(
            username=update_data.username,
            email=update_data.email,
            address=update_data.address,
            description=update_data.description,
            occupation=update_data.occupation,
            phone_number=update_data.phone_number,
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

    def _get_by_id(self, model_id: str) -> Union["UserModel", None]:
        return self.session.query(UserModel).filter(UserModel.id == model_id).first()

    def _get_all(self) -> list[ModelBase]:
        return self.session.query(UserModel).all()

    def _update(
        self,
        username: str = "",
        phone_number: str = "",
        address: str = "",
        occupation: str = "",
        description: str = "",
        email: str = "",
        password: str = "",
    ):
        if len(username) != 0:
            self.username = username
        if len(phone_number) != 0:
            self.phone_number = phone_number
        if len(address) != 0:
            self.address = address
        if len(occupation) != 0:
            self.occupation = occupation
        if len(description) != 0:
            self.description = description
        if len(email) != 0:
            self.email = email
        if len(password) != 0:
            self._set_password(password)
        self.update_at = datetime.now()
