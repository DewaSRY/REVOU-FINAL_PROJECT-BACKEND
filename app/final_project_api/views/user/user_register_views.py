"""_summary_

Returns:
    _type_: _description_
"""

from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus

from app.final_project_api.model.user import (
    UserModel,
)

from .user_blp import blp
from .user_data import (
    AuthData,
    AuthResponseData,
)
from .user_schemas import UserModelSchema, RegisterSchema

from app.jwt_service import createAccessToken


@blp.route("/register")
class UserRegisterView(MethodView):
    @blp.arguments(schema=RegisterSchema)
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserModelSchema)
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
