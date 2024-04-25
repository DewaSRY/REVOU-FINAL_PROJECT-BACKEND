"""_summary_
"""

from .user_type_data import UserTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from app.model_base_service import db, ModelBaseService


class UserTypeModel(UserTypeData, ModelBaseService["UserTypeModel"], db.Model):
    __tablename__ = "user_type"
    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column("name", String(20), unique=True)

    def _delete(self):
        self.session.delete(self)
