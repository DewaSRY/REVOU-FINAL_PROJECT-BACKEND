"""_summary_
"""

from .business_data import BusinessTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from app.model_base_service import ModelBaseService, db
from typing import Union


class BusinessTypeModel(
    BusinessTypeData, ModelBaseService["BusinessTypeModel"], db.Model
):
    __tablename__ = "business_type"
    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column("name", String(50), unique=True)

    def _get_all_model(self):
        return self.session.query(BusinessTypeModel).all()

    def _get_model_by_id(self, model_id: int) -> "BusinessTypeModel":
        return (
            self.session.query(BusinessTypeModel)
            .filter(BusinessTypeModel.id == model_id)
            .first()
        )

    def getStore(self):
        return self.name

    @classmethod
    def get_match_model_by_name(
        cls, model_name: str
    ) -> Union["BusinessTypeModel", None]:
        """_summary_
        Returns:
            Union["BusinessTypeModel", None]: _description_
        """
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
    def add_model(cls, name: str) -> "BusinessTypeModel":
        """add_model
        Args:
            name (str): put the business name
        Raises:
            Exception: _description_
        Returns:
            BusinessTypeModel: BusinessTypeModel
        """
        try:
            model = BusinessTypeModel(name=name)
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            print(e)
            raise Exception(f"failed to add Business type with name : {name}")
