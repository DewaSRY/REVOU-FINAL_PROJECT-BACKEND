
from .sql_model_instance import SQLModelInstance

class ModelBase: 
    """ModelBase
      base model use as interface how receive service from `ModelBaseService` 
      class
      current method: 
        - `_update`
        - `_delete`
    """
    def _update(self, **args)->None:
      "use as mark to receive model base service update "
      raise Exception(f"{self.__class__} _update not implement")
    
    def _delete(self):
      raise Exception(f"{self.__class__} _delete not implement, need to implement this method to receive the service")
    
