"""_summary_
"""

from .business_type_data import BusinessTypeData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from app.model_base_service import ModelBaseService, db


class BusinessTypeModel(
    BusinessTypeData, ModelBaseService["BusinessTypeModel"], db.Model
):
    __tablename__ = "business_type"
    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column("name", String(50))
