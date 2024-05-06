"""_summary_
"""

from .data import UserTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from app.model_base_service import db, ModelBaseService


class UserTypeModel(UserTypeData, ModelBaseService["UserTypeModel"], db.Model):
    __tablename__ = "user_type"
    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column("name", String(20), unique=True)

    def _delete(self):
        self.session.delete(self)

    def _get_model_by_id(self, model_id: int) -> "UserTypeModel":
        model = (
            self.session.query(UserTypeModel)
            .filter(UserTypeModel.id == model_id)
            .first()
        )
        return model

    def _get_all_model(self) -> list["UserTypeModel"]:
        return self.session.query(UserTypeModel).all()

    @classmethod
    def get_available_type(cls):
        typList: UserTypeModel = UserTypeModel.get_all_model()
        return [model.name for model in typList]

    @classmethod
    def add_model(cls, name: str) -> "UserTypeModel":
        try:
            model = UserTypeModel(name=name)
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            print(e)
