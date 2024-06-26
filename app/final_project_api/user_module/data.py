"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime
from dataclasses import dataclass, field
from passlib.hash import pbkdf2_sha256

from app.model_base_service import DataBaseDefault
from app.image_upload_service import ImageData

from app.final_project_api.business_module.data import BusinessData
from app.final_project_api.product_module.data import ProductData


@dataclass
class UserImageData(ImageData):

    user_id: str = field(default_factory=str)
    username: str = field(default_factory=str)

    def __init__(self, public_id: str, secure_url: str, user_id: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.user_id = user_id


@dataclass
class UserTypeData:
    id: str = field(init=False)
    name: str


@dataclass
class UserData(DataBaseDefault):

    phone_number: str = field(init=False, default_factory=str)
    address: str = field(init=False, default_factory=str)
    occupation: str = field(init=False, default_factory=str)
    description: str = field(init=False, default_factory=str)

    profile_url: str = field(default_factory=str)

    images: list[UserImageData] = field(init=False, default_factory=list)

    user_type_id: int = field(init=False)
    user_type: str = field(init=False)
    business: list[BusinessData] = field(init=False, default_factory=list, repr=False)
    product: list[ProductData] = field(init=False, default_factory=list, repr=False)
    business_amount: int = field(init=False)
    product_amount: int = field(init=False)
    username: str = field(default="")
    password: str = field(default="")
    email: str = field(default="")

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
        """match_password"""
        return pbkdf2_sha256.verify(secret=receive_password, hash=self.password)


@dataclass
class AuthData:
    """AuthData"""

    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    password: str = field(default_factory=str)

    def getCredential(self) -> str:
        """getCredential"""

        if len(self.email) == 0:
            return f"username: '{self.username}'"
        elif len(self.username) == 0:
            return f"email: '{self.email}'"
        else:
            return f"username : '{self.username}',email: '{self.email}'  "

    def passwordNotMatchMessage(self):
        """passwordNotMatchMessage"""

        return (
            f"password:'{self.password}' not match with account {self.getCredential()}"
        )


@dataclass
class UserUpdateData:
    """UserUpdateData"""

    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    phone_number: str = field(default_factory=str)
    address: str = field(default_factory=str)
    occupation: str = field(default_factory=str)
    description: str = field(default_factory=str)


@dataclass
class AuthResponseData(UserUpdateData):
    """AuthResponseData"""

    access_token: str = field(default_factory=str)

    user_id: str = field(default_factory=str)
    create_at: datetime = field(default_factory=datetime)
    update_at: datetime = field(default_factory=datetime)

    user_type: str = field(default_factory=str)
    profile_url: str = field(default_factory=str)
    images: list[str] = field(default_factory=list)

    business: list["BusinessData"] = field(default_factory=list, repr=False)
    product: list["ProductData"] = field(default_factory=list, repr=False)
    business_amount: int = field(default_factory=str)
    product_amount: int = field(default_factory=str)

    def __init__(self, user_model: UserData, access_token: str):
        super().__init__(
            address=user_model.address,
            description=user_model.description,
            occupation=user_model.occupation,
            email=user_model.email,
            phone_number=user_model.phone_number,
            username=user_model.username,
        )
        self.user_id = user_model.id
        self.create_at = user_model.create_at
        self.update_at = user_model.update_at
        self.access_token = access_token
        self.user_type = user_model.user_type
        self.images = user_model.images
        self.business = user_model.business
        self.product = user_model.product
        self.profile_url = user_model.profile_url
        self.product_amount = user_model.product_amount
        self.business_amount = user_model.business_amount
