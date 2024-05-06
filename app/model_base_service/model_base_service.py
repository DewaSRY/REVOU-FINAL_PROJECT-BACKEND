"""_summary_
Returns:
    _type_: _description_
"""

from .db import db
from .model_base import ModelBase
from typing import Iterable
from typing import Union
from sqlalchemy.orm.session import Session
from typing import Self


class ModelBaseService(ModelBase):
    session: Session = db.session

    def _delete(self):
        self.session.delete(self)

    @classmethod
    def setSession(cls, session: Session) -> None:
        cls.session = session

    @classmethod
    def add(cls, model: Self) -> Self:
        try:
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            raise Exception(f"{cls.__call__} failed to add model")

    @classmethod
    def getById(cls, model_id: Union[str, int]):
        return cls._getById(cls, model_id=model_id)

    @classmethod
    def update(cls, model: Self, **args) -> Self:
        try:
            model._update(**args)
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            raise e

    @classmethod
    def delete(cls, model: Self) -> "ModelBaseService":
        try:
            model._delete()
            cls.session.commit()
            return model
        except Exception as e:
            raise e

    @classmethod
    def updateWithId(cls, model_id: Union[str, int], **args):
        model: Self = cls._getById(cls, model_id=model_id)
        cls.update(model=model, **args)
        return model

    @classmethod
    def deleteModelWithId(cls, model_id: Union[str, int]):
        model: Self = cls._getById(cls, model_id=model_id)
        cls.delete(model=model)

    @classmethod
    def get_all_model(cls: Self) -> list[Self]:
        return cls._getAll(cls)

    @classmethod
    def cleanAll(cls):
        all_model_to_clean: list[Self] = cls._getAll(cls)
        for model in all_model_to_clean:
            model._delete()
            cls.session.commit()
