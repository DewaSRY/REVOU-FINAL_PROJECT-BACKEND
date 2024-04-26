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
            print(item_data)
            user = UserModel.add_model(
                UserModel(
                    email=item_data.email,
                    username=item_data.username,
                    password=item_data.password,
                )
            )

            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=7)
            )
            return AuthResponseData(user_model=user, access_token=access_token)
        except Exception as E:
            print(E)
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message="error while create",
            )
