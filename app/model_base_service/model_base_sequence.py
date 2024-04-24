"""_summary_
"""


from .model_base import ModelBase

class ModelBaseSequence:
    """ModelBaseSequence
    - _clean_up_all_model
    """
    
    def _clean_up_all_model(self) -> list[ModelBase] :
      raise Exception(f"{self.__class__} not implement _clean_up_all_model ")