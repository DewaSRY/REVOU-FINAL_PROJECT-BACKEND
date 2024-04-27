"""_summary_
"""

from app.model_base_service import DataBaseDefault
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ProductData(DataBaseDefault):
    product_name: str
    product_price: float
    product_images: list[str] = field(init=False, default_factory=list)
    business_id: str
    user_id: str
    business_name: str = field(init=False, default_factory=str)
    username: str = field(init=False, default_factory=str)

    def __init__(self, product_name: str, product_price: float, business_id: str):
        super().__init__()
        self.product_name = product_name
        self.product_price = product_price
        self.business_id = business_id
        self._set_user_id()

    def _set_user_id(self):
        raise Exception(f"{self.__class__} not implement _set_user_id ")
