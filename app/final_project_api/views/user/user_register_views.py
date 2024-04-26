"""_summary_

Returns:
    _type_: _description_
"""

from flask_smorest import abort
from flask.views import MethodView
from .user_blp import blp
from http import HTTPStatus
from datetime import timedelta
from app.final_project_api.model.user import (
    UserModel,
    RegisterSchema,
    AuthData,
    AuthResponseData,
    AuthResponseSchema,
)
from flask_jwt_extended import (
    create_access_token,
)
from app.model_base_service import db

from app.jwt_service import createAccessToken


@blp.route("/user/register")
class UserRegisterView(MethodView):
    @blp.arguments(schema=RegisterSchema)
    @blp.response(status_code=HTTPStatus.CREATED, schema=AuthResponseSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description="duplicate username",
    )
    def post(self, item_data: AuthData):
        """_summary_
        Args:
            item_data (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            user = UserModel.add_model(
                email=item_data.email,
                username=item_data.username,
                password=item_data.password,
            )
            access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
            return AuthResponseData(user_model=user, access_token=access_token)
        except Exception as E:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=str(E),
            )
