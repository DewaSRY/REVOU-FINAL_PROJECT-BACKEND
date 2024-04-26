"""_summary_

Returns:
    _type_: _description_
"""

from marshmallow import Schema, fields


class LoginSchemas(Schema):
    __name__ = "user base schemas"
    username = fields.String()
    password = fields.String()


class UserRegisterSchema(LoginSchemas):
    """payload to create schemas"""

    email = fields.Str()


class UseResponseSchema(UserRegisterSchema):
    """schemas to response user schemas"""

    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
