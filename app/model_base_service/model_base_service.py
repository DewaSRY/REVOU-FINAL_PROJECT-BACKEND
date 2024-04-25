"""_summary_
Returns:
    _type_: _description_
"""
from .db import db
from .session_type import SESSION_TYPE
from .model_base import ModelBase
from typing import Iterable
from typing import Union

class ModelBaseService[T](ModelBase):
    """ModelBaseService
    will provide several class method can help to work with the data base
    """
    session: SESSION_TYPE = db.session

    @classmethod
    def set_session(cls, session: SESSION_TYPE) -> None:
        """set_session
        Args:
            session (SESSION_TYPE): _description_
        """
        cls.session = session

    @classmethod
    def add_model(cls, model: T)-> T:
        """add_model
        Args:
            model (T):T
        Returns: 
            return T
        """
        try:
            cls.session.add(model)
            cls.session.commit()
            return model
        except Exception as e:
            raise Exception(f"{cls.__call__} failed to add model")
    
    @classmethod 
    def update_with_id(cls, model_id:Union[str, int] ,**args ):
        model:T=cls\
            ._get_model_by_id(cls, model_id=model_id)
        cls.update_model( model=model, **args)
    
    @classmethod
    def delete_model_with_id(cls, model_id: Union[str, int]):
        """delete_model_with_id
        Args:
            model_id (Union[str, int]): _description_
        """
        model:T=cls\
            ._get_model_by_id(cls, model_id= model_id)
        cls.delete_model(model= model)
    
    @classmethod
    def get_model_by_id(cls, model_id: Union[str, int]):
        return cls._get_model_by_id(cls, model_id= model_id)
    
    @classmethod 
    def add_all_model(cls, list_model: Iterable[T]) -> list[T]:
        try:
            cls.session.add_all(instances= list_model)
            cls.session.commit()
            return list_model
        except Exception as e:
            raise Exception(f"{cls.__class__} failed to add_all_model")


    @classmethod
    def update_model(cls, model: T,  **args) -> T:
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
    def delete_model(cls, model: T):
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
        