"""_summary_
"""

from dataclasses import dataclass, field
from app.model_base_service import DataBaseDefault


@dataclass(kw_only=True)
class BusinessDate(DataBaseDefault):
    user_id: str
    business_name: str

    business_types: str = field(init=False, compare=False)
    business_type_id: int = field(init=False)
    business_images: list[str] = field(init=False, default_factory=list)

    def __init__(self, user_id: str, business_name: str, business_type_name: str):
        super().__init__()
        self.user_id = user_id
        self.business_name = business_name
        self._set_match_business_type(business_type_name=business_type_name)
        # self.business_images = []

    def _set_match_business_type(self, business_type_name: str):
        raise Exception(f"{self.__class__} not implement _set_match_business_type ")
