"""_summary_

Returns:
    _type_: _description_
"""

from app.model_base_service import (
    db,
    ModelBaseService,
)
from sqlalchemy import (
    String,
    Integer,
)
from sqlalchemy.orm import mapped_column
from .mock_data import MockData
from typing import Union, Self


class MockModelBase(MockData, ModelBaseService, db.Model):
    id = mapped_column("data_id", Integer, primary_key=True)
    name = mapped_column("name", String(50))
    username = ""

    def __init__(self, name: str) -> None:
        self.name = name

    def _update(self, name) -> None:
        "use as mark to receive model base service update"
        self.name = name

    def _get_by_id(self, model_id: int) -> Union[None, Self]:
        return (
            self.session.query(MockModelBase)
            .filter(MockModelBase.id == model_id)
            .first()
        )

    def _delete(self):
        self.session.delete(self)

    def _get_all(self) -> list[Self]:
        return self.session.query(MockModelBase).all()
