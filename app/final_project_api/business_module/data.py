"""_summary_
"""

from dataclasses import dataclass, field
from app.model_base_service import DataBaseDefault
from app.final_project_api.product_module.data import ProductData
from app.image_upload_service import ImageData


@dataclass
class BusinessImageData(ImageData):
    business_id: str = field(default_factory=str)

    def __init__(self, public_id: str, business_id: str, secure_url: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.business_id = business_id


@dataclass
class BusinessTypeData:
    id: int = field(init=False)
    name: str

    def __init__(self, name: str):
        self.name = name


@dataclass(kw_only=True)
class BusinessDate(DataBaseDefault):
    user_id: str
    business_name: str
    business_types: str = field(init=False, compare=False)
    description: str = field(default="")

    business_type_id: int = field(init=False)
    business_images: list[BusinessImageData] = field(init=False, default_factory=list)
    product: list[ProductData] = field(init=False, default_factory=list)
    profile_url: str = field(default_factory=str)

    username: str = field(init=False, default_factory=str)
    user_phone_number: str = field(init=False, default_factory=str)
    user_email: str = field(init=False, default_factory=str)
    is_delete: bool = field(default=False, init=False)

    def __init__(
        self,
        user_id: str,
        business_name: str,
        business_type_name: str,
        description: str,
    ):
        super().__init__()
        self.user_id = user_id
        self.business_name = business_name
        self._set_match_business_type(business_type_name=business_type_name)
        self.description = description
        self.profile_url = ""
        self.is_delete = False

    def _set_match_business_type(self, business_type_name: str):
        raise Exception(f"{self.__class__} not implement _set_match_business_type ")


@dataclass
class BusinessCreateData:
    business_name: str = field(default_factory=str)
    business_types: str = field(default_factory=str)
    description: str = field(default_factory=str)
