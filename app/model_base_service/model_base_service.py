"""_summary_
Returns:
    _type_: _description_
"""
from .db import db
from .session_type import SESSION_TYPE
from .model_base import ModelBase
from typing import Iterable
from .model_base_instance import ModelBaseInstance
from .model_base_sequence import ModelBaseSequence

class ModelBaseService[ModelBaseInstance](ModelBase):
    """ModelBaseService
    will provide several class method can help to work with the data base
    """
    session: SESSION_TYPE = db.session

    @classmethod
    def set_session(cls, session: SESSION_TYPE) -> None:
        """_summary_
        Args:
            session (SESSION_TYPE): _description_
        """
        cls.session = session

    @classmethod
    def add_model(cls, model: ModelBaseInstance)-> ModelBaseInstance:
        """add_model
        Args:
            model (T):ModelBaseInstance
        Returns: 
            return ModelBaseInstance
        """
        try:
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            raise e
      

    @classmethod 
    def add_all_model(cls, list_model: Iterable[ModelBaseInstance]) -> list[ModelBaseInstance]:
        try:
            cls.session.add_all(instances= list_model)
            cls.session.commit()
            return list_model
        
        except Exception as e:
            raise e


    @classmethod
    def update_model(cls, model: ModelBaseInstance,  **args) -> ModelBaseInstance:
        """_summary_
        Args:
            model (T): _description_
        Returns:
            T: _description_
        """
        try:
            model._update(**args)
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            raise e

    @classmethod
    def delete_model(cls, model: ModelBaseInstance):
        try:
            model._delete()
            cls.session.commit()
        except Exception as e:
            raise e
    
    @classmethod 
    def clean_all_model(cls):
        """clean_all_model
        use to delete all model 
        """
        all_model_to_clean:list[ModelBase]=cls._clean_up_all_model(cls)
        for model in all_model_to_clean:
            model._delete()
            cls.session.commit()
        