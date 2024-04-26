"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from .user_blp import blp
from http import HTTPStatus
from datetime import timedelta
from app.final_project_api.model.user import (
    UserModel,
    LoginSchemas,
    AuthData,
    AuthResponseData,
    AuthResponseSchema,
)
from app.datetime_service import getDateTimeLimit
from app.jwt_service import createAccessToken
from flask_jwt_extended import (
    create_access_token,
)

# from pprint import pprint


@blp.route("/user/login")
class UserLoginViews(MethodView):

    @blp.arguments(schema=LoginSchemas)
    @blp.response(schema=AuthResponseSchema, status_code=HTTPStatus.OK)
    @blp.alt_response(
        status_code=HTTPStatus.FORBIDDEN,
        description="user not found",
    )
    def post(self, user_data: AuthData):
        """_summary_
        Args:
            user_data (_type_): _description_
        Returns:
            _type_: _description_
        """
        user: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )

        if user and user.match_password(receive_password=user_data.password):
            access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
            return AuthResponseData(user_model=user, access_token=access_token)

        abort(http_status_code=HTTPStatus.FORBIDDEN, message="Invalid credentials")
