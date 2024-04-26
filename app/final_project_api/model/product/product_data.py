"""_summary_
"""

from model_base_service import DataBaseDefault
from dataclasses import dataclass, field


@dataclass
class ProductData(DataBaseDefault):
    product_name: str
    product_price: float
    product_images: list[str] = field(init=False, default_factory=list)
