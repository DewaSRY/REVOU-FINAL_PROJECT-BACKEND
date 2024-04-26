"""_summary_
"""

from app.model_base_service.db import Base
from .user_type_data import UserTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from app.model_base_service import db, ModelBaseService
from app.data_store_service import DataStoreable


class UserTypeModel(
    UserTypeData, ModelBaseService["UserTypeModel"], DataStoreable[str], db.Model
):
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
        print(f"type id is {model_id} model is {model}")

        return model

    def get_store(self) -> str:
        return self.name
