from dataclasses import dataclass, field
from app.model_base_service import DataBaseDefault
from .user_image_data import UserImageData
from .user_type_data import UserTypeData
from app.final_project_api.model.business import BusinessDate
from app.final_project_api.model.product import ProductData
from passlib.hash import pbkdf2_sha256


@dataclass
class UserData(DataBaseDefault):
    username: str
    password: str
    email: str
    profile_url: str = field(default_factory=str)
    user_images: list[str] = field(init=False, default_factory=list)
    user_type_id: int = field(init=False)
    user_type: str = field(init=False)
    business: list[BusinessDate] = field(init=False, default_factory=list, repr=False)
    product: list[ProductData] = field(init=False, default_factory=list, repr=False)
    product_amount: int = field(init=False)
    business_amount: int = field(init=False)

    phone_number: str = field(init=False, default_factory=str)
    address: str = field(init=False, default_factory=str)
    occupation: str = field(init=False, default_factory=str)
    description: str = field(init=False, default_factory=str)

    def __init__(self, username: str, email: str, password: str):
        super().__init__()
        self.username = username
        self.email = email
        self._set_password(password)
        self.user_type_id = 1
        self.profile_url = ""

        self.phone_number = ""
        self.address = ""
        self.occupation = ""
        self.description = ""

    def _set_password(self, password: str) -> None:
        self.password = pbkdf2_sha256.hash(password)

    def match_password(self, receive_password: str) -> bool:
        return pbkdf2_sha256.verify(secret=receive_password, hash=self.password)
