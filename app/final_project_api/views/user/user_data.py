"""_summary_
"""

from dataclasses import dataclass, field
from app.final_project_api.model.business import BusinessDate
from app.final_project_api.model.product import ProductData
from app.final_project_api.model.user import UserData
from datetime import datetime


@dataclass
class AuthData:
    password: str
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)


@dataclass
class UserUpdateData:
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)

    phone_number: str = field(default_factory=str)
    address: str = field(default_factory=str)
    occupation: str = field(default_factory=str)
    description: str = field(default_factory=str)


@dataclass
class AuthResponseData(UserUpdateData):
    access_token: str = field(default_factory=str)

    user_id: str = field(default_factory=str)
    user_type: str = field(default_factory=str)
    create_at: datetime = field(default_factory=datetime)
    update_at: datetime = field(default_factory=datetime)

    profile_url: str = field(default_factory=str)
    images: list[str] = field(default_factory=list)

    business: list["BusinessDate"] = field(default_factory=list, repr=False)
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
        self.images = user_model.user_images
        self.business = user_model.business
        self.product = user_model.product
        self.profile_url = user_model.profile_url
        self.product_amount = user_model.product_amount
        self.business_amount = user_model.business_amount
