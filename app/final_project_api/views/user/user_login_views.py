"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from .user_blp import blp
from http import HTTPStatus
from datetime import timedelta
from app.final_project_api.model.user import UserModel, LoginSchemas
from app.datetime_service import getDateTimeLimit
from flask_jwt_extended import (
    create_access_token,
)
from pprint import pprint


@blp.route("/login")
class UserLoginViews(MethodView):

    @blp.arguments(schema=LoginSchemas)
    @blp.alt_response(
        HTTPStatus.UNAUTHORIZED,
        description="user not found",
    )
    def post(self, user_data):
        """_summary_
        Args:
            user_data (_type_): _description_
        Returns:
            _type_: _description_
        """
        user: UserModel = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and user.match_password(receive_password=user_data["password"]):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=7)
            )
            return {
                "access_token": access_token,
            }
        abort(http_status_code=HTTPStatus.UNAUTHORIZED, message="Invalid credentials")
