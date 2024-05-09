"""_summary_
"""

from math import ceil
from dataclasses import dataclass, field

from app.model_base_service import DataBaseDefault
from app.image_upload_service import ImageData
from app.util.query_data import QueryData


@dataclass
class ProductImageData(ImageData):
    product_id: str = field(default_factory=str)

    def __init__(self, public_id: str, product_id: str, secure_url: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.product_id = product_id


@dataclass(kw_only=True)
class ProductData(DataBaseDefault):
    product_name: str
    product_price: float
    product_images: list[ProductImageData] = field(init=False, default_factory=list)
    business_id: str
    user_id: str
    business_name: str = field(init=False, default_factory=str)
    username: str = field(init=False, default_factory=str)
    profile_url: str = field(default="")
    is_delete: bool = field(default=False)
    description: str = field(default="")

    def __init__(
        self,
        product_name: str,
        product_price: float,
        business_id: str,
        description: str,
    ):
        super().__init__()
        self.business_id = business_id
        self.profile_url = ""
        self._set_user_id()
        self.product_name = product_name
        self.product_price = product_price
        self.description = description

    def _set_user_id(self):
        raise Exception(f"{self.__class__} not implement _set_user_id ")


@dataclass
class ProductUpdateData:
    product_name: str
    product_price: float
    description: str


@dataclass
class ProductCreateData(ProductUpdateData):
    business_id: str


@dataclass
class PublicProduct(QueryData):
    data: list[ProductData] = field(default_factory=list)

    @property
    def total_data(cls):
        from .model import ProductModel

        modelAmount = ProductModel.total_row()
        return modelAmount

    @property
    def total_page(self):
        from .model import ProductModel

        modelAmount = ProductModel.total_row()
        return ceil(modelAmount / self.limit)

    def __init__(self, queryData: QueryData, productList: list[ProductData]):
        super().__init__(
            page=queryData.page, limit=queryData.limit, search=queryData.search
        )
        self.data = productList
