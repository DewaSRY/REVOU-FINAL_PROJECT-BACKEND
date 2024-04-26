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
from flask_jwt_extended import (
    jwt_required,
)
from sqlalchemy.exc import SQLAlchemyError


@blp.route("/user/<string:user_id>")
class UserWithIdViews(MethodView):

    @jwt_required()
    @blp.response(status_code=HTTPStatus.OK, schema=UseResponseSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description="user not found",
    )
    def get(self, user_id):
        """_summary_
        Args:
            user_id (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            return UserModel.get_model_by_id(user_id=user_id)
        except Exception as E:
            abort(http_status_code=HTTPStatus.NOT_FOUND, message="user not found")

    @jwt_required()
    @blp.arguments(schema=UserRegisterSchema)
    @blp.response(status_code=HTTPStatus.ACCEPTED, schema=UseResponseSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT, description="error while update the animal"
    )
    def put(self, item_data, user_id):
        """_summary_
        Args:
            item_data (_type_): _description_
            user_id (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            return UserModel.update_with_id(model_id=user_id, **item_data)

        except SQLAlchemyError as E:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message="error while update the animal",
            )
