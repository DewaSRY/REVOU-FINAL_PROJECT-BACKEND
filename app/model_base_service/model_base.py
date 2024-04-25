from typing import Union
from .db import Base


class ModelBase:
    """ModelBase
    base model use as interface how receive service from `ModelBaseService`
    class
    current method:
      - `_update`
      - `_delete`
    """

    def _update(self, **args) -> None:
        "use as mark to receive model base service update"
        raise Exception(f"{self.__class__} _update not implement")

    def _delete(self):
        raise Exception(
            f"{self.__class__} _delete not implement, need to implement this method to receive the service"
        )

    def _clean_up_all_model(self):
        raise Exception(f"{self.__class__} not implement __clean_up_all_model")

    def _get_model_by_id(self, model_id: Union[str, int]) -> Union[Base, None]:
        raise Exception(f"{self.__class__} not implement _get_model_by_id")
