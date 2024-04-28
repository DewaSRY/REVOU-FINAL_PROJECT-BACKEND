"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus

from app.final_project_api.model.user import (
    UserModel,
)
from app.jwt_service import createAccessToken

from .user_blp import blp
from .user_data import (
    AuthData,
    AuthResponseData,
)
from .user_schemas import (
    LoginSchemas,
    UserModelSchema,
)


@blp.route("/login")
class UserLoginViews(MethodView):

    @blp.arguments(schema=LoginSchemas)
    @blp.response(schema=UserModelSchema, status_code=HTTPStatus.OK)
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
        # print(user.match_password(receive_password=user_data.password))
        if user and user.match_password(receive_password=user_data.password):

            access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
            return AuthResponseData(user_model=user, access_token=access_token)

        abort(http_status_code=HTTPStatus.FORBIDDEN, message="Invalid credentials")
