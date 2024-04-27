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
class AuthResponseData:
    user_id: str
    create_at: datetime
    update_at: datetime
    access_token: str
    user_type: str
    images: list[str]
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    business: list["BusinessDate"] = field(default_factory=list, repr=False)
    product: list["ProductData"] = field(default_factory=list, repr=False)

    def __init__(self, user_model: UserData, access_token: str):
        self.user_id = user_model.id
        self.create_at = user_model.create_at
        self.update_at = user_model.update_at
        self.access_token = access_token
        self.email = user_model.email
        self.username = user_model.username
        self.user_type = user_model.user_type
        self.images = user_model.user_images
        self.business = user_model.business
        self.product = user_model.product
