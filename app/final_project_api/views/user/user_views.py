"""_summary_

Returns:
    _type_: _description_
"""

from flask_smorest import abort
from flask.views import MethodView
from .user_blp import blp
from http import HTTPStatus
from ...model.user import (
    UserRegisterSchema,
    UseResponseSchema,
    UserModel,
)


@blp.route("/user")
class UserView(MethodView):
    @blp.arguments(schema=UserRegisterSchema)
    @blp.response(status_code=HTTPStatus.CREATED, schema=UseResponseSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description="duplicate username",
    )
    def post(self, item_data):
        """_summary_
        Args:
            item_data (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            return UserModel.add_model(UserModel(**item_data))
        except Exception as E:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message="error while create: duplicate user name",
            )
