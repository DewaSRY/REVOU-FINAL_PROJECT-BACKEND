from typing import Union

from typing import Self


class ModelBase:
    def _update(self, **args) -> None:
        raise Exception(f"{self.__class__} _update not implement")

    def _delete(self):
        raise Exception()

    def _getAll(self) -> list[Self]:
        raise Exception(f"{self.__class__} not implement __get_all_model")

    def _getById(self, model_id: Union[str, int]) -> Union[Self, None]:
        raise Exception(f"{self.__class__} not implement _get_model_by_id")
