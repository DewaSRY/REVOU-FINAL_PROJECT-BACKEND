"""_summary_
"""

from .data import BusinessTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from app.model_base_service import ModelBaseService, db
from typing import Union, Self


class BusinessTypeModel(BusinessTypeData, ModelBaseService, db.Model):
    __tablename__ = "business_type"
    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column("name", String(50), unique=True)

    def _get_all(self) -> list[Self]:
        return self.session.query(BusinessTypeModel).all()

    def _get_by_id(self, model_id: int) -> Self:
        return (
            self.session.query(BusinessTypeModel)
            .filter(BusinessTypeModel.id == model_id)
            .first()
        )

    @classmethod
    def get_match_model_by_name(cls, model_name: str) -> Union[Self, None]:
        return (
            cls.session.query(BusinessTypeModel)
            .filter(BusinessTypeModel.name.like(model_name))
            .first()
        )

    @classmethod
    def get_available_type(cls):
        typList: BusinessTypeModel = BusinessTypeModel.get_all_model()
        return [model.name for model in typList]

    @classmethod
    def add_model(cls, name: str) -> Self:
        try:
            model = BusinessTypeModel(name=name)
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            print(e)
            raise Exception(f"failed to add Business type with name : {name}")
