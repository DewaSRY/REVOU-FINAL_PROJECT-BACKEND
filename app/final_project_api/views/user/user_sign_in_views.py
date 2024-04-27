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
)
from ...schema.user import (
    RegisterSchema,
    AuthData,
    AuthResponseData,
    UserModelSchema,
)
from app.jwt_service import createAccessToken, getCurrentAuthId
from flask_jwt_extended import jwt_required


@blp.route("/user/sign-in")
class UserSignInView(MethodView):

    @jwt_required()
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description="duplicate username",
    )
    def get(self):
        try:
            user = UserModel.get_model_by_id(model_id=getCurrentAuthId())
            access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
            return AuthResponseData(user_model=user, access_token=access_token)
        except Exception as E:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=str(E),
            )
