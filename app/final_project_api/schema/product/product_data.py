"""_summary_
"""

from dataclasses import dataclass, field


@dataclass
class ProductCreateData:
    product_name: str
    product_price: float
    business_id: str
