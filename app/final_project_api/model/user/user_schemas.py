"""_summary_
"""

from marshmallow import Schema, fields, post_load
from dataclasses import dataclass, field
from .user_data import UserData
from datetime import datetime


@dataclass
class AuthData:
    password: str
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)


class LoginSchemas(Schema):
    __name__ = "user base schemas"
    username = fields.String()
    password = fields.String(required=True)
    email = fields.Email()

    @post_load
    def get_data_login(self, data, **kwargs):
        return AuthData(**data)


class RegisterSchema(Schema):
    """payload to create schemas"""

    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)

    @post_load
    def get_data_register(self, data, **kwargs):
        return AuthData(**data)


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

    def __init__(self, user_model: UserData, access_token: str):
        self.user_id = user_model.id
        self.create_at = user_model.create_at
        self.update_at = user_model.update_at
        self.access_token = access_token
        self.email = user_model.email
        self.username = user_model.username
        self.user_type = user_model.user_type
        self.images = user_model.user_images


class AuthResponseSchema(RegisterSchema):
    """schemas to response user schemas"""

    user_id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    access_token = fields.Str()

    email = fields.Email()
    username = fields.Str()
    user_type = fields.Str()
    images = fields.List(fields.Str)
