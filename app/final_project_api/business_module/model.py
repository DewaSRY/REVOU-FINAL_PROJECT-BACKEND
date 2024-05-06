"""_summary_
"""

from .data import BusinessDate, BusinessCreateData
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, String, Boolean, DateTime
from app.model_base_service import db, ModelBaseService
from app.message_service import MessageService
from app.util import QueryData, QuerySchema
from datetime import datetime


class BusinessModel(BusinessDate, ModelBaseService, db.Model):
    __tablename__ = "business"
    id = mapped_column("business_id", String(36), primary_key=True)
    user_id = mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    business_name = mapped_column("name", String(50))
    description = mapped_column("description", String(50))
    profile_url = mapped_column("profile_url", String(50))
    is_delete = mapped_column("is_delete", Boolean, default=False)
    create_at = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    update_at = mapped_column(
        "updated_at", DateTime(timezone=True), onupdate=datetime.now
    )
    business_type_id = mapped_column(
        "business_type_id", String(36), ForeignKey("business_type.id")
    )

    @property
    def business_images(self):
        from .image_model import BusinessImageModel

        imagesList = BusinessImageModel.get_by_business_id(self.id)
        if len(imagesList) == 0:
            return []
        return imagesList

    @property
    def product(self):
        from app.final_project_api.product_module.model import ProductModel as PM

        return PM.get_by_business_id(business_id=self.id)

    @property
    def business_types(self):
        from .type_model import BusinessTypeModel as BTM

        model: BTM = BTM.get_by_id(model_id=self.business_type_id)
        return model.name

    @property
    def user_phone_number(self):
        from app.final_project_api.user_module.model import UserModel

        return UserModel.get_by_id(model_id=self.user_id).phone_number

    @property
    def username(self):
        from app.final_project_api.user_module.model import UserModel

        return UserModel.get_by_id(model_id=self.user_id).username

    @property
    def user_email(self):
        from app.final_project_api.user_module.model import UserModel

        return UserModel.get_by_id(model_id=self.user_id).email

    def _update(
        self,
        business_name: str = "",
        business_type_name: str = "",
        description: str = "",
    ) -> None:
        if len(business_name) != 0:
            self.business_name = business_name
        if len(business_type_name) != 0:
            self.business_type_name = business_type_name
        if len(description) != 0:
            self.description = description

    def _set_match_business_type(self, business_type_name: str):
        from .type_model import BusinessTypeModel

        businessType: BusinessTypeModel = BusinessTypeModel.get_match_model_by_name(
            model_name=business_type_name
        )
        if businessType == None:
            message = MessageService.get_message("business_typ_not_found").format(
                f"{business_type_name} not in available list:   "
            )
            raise Exception(message)
        self.business_type_id = businessType.id

    def _get_all(self):
        return self.session.query(BusinessModel).all()

    def _get_by_id(self, model_id: str) -> "BusinessModel":
        return (
            self.session.query(BusinessModel)
            .filter(BusinessModel.id == model_id)
            .first()
        )

    @classmethod
    def delete_by_id(cls, model_id: str):
        from app.final_project_api.product_module.model import ProductModel

        businessModel: BusinessModel = BusinessModel.get_by_id(model_id=model_id)
        businessModel.is_delete = True
        productList: list[ProductModel] = businessModel.product
        for product in productList:
            product.is_delete = True

        cls.session.add(businessModel)
        cls.session.commit()
        return businessModel

    @classmethod
    def update_by_id(cls, business_id: str, update_data: BusinessCreateData):
        businessModel: BusinessModel = BusinessModel.get_by_id(model_id=business_id)
        businessModel._update(
            business_name=update_data.business_name,
            business_type_name=update_data.business_types,
            description=update_data.description,
        )
        cls.session.add(businessModel)
        cls.session.commit()
        return businessModel

    @classmethod
    def get_all_public(cls, query_data: QueryData = QueryData()):
        queryPointer = cls.session.query(BusinessModel)
        if len(query_data.search) != 0:
            return (
                queryPointer.filter(BusinessModel.is_delete == False)
                .filter(BusinessModel.business_name.like(query_data.search))
                .all()
            )
        offset = (query_data.page - 1) * query_data.limit
        return (
            queryPointer.filter(BusinessModel.is_delete == False)
            .limit(query_data.limit)
            .offset(offset)
            .all()
        )

    @classmethod
    def get_by_user_id(cls, user_id: str) -> list["BusinessModel"]:
        return (
            cls.session.query(BusinessModel)
            .filter(BusinessModel.user_id == user_id)
            .all()
        )

    @classmethod
    def add_model(
        cls,
        user_id: str,
        business_name: str,
        business_type_name: str,
        description: str,
    ) -> "BusinessModel":

        model: BusinessModel
        try:
            model = BusinessModel(
                user_id=user_id,
                business_name=business_name,
                business_type_name=business_type_name,
                description=description,
            )
        except Exception as e:
            raise e
        cls.session.add(model)
        cls.session.commit()
        return model
