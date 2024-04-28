"""_summary_
"""

from cloudinary.utils import cloudinary_url
from http import HTTPStatus

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_smorest.fields import Upload
from flask_jwt_extended import jwt_required

from app.final_project_api.model.user import UserModel, UserImageModel
from app.jwt_service import createAccessToken, getCurrentAuthId
from app.image_upload_service import (
    ImageService,
    ImageSchema,
    ImageData,
    ImagesPayloadData,
)

from .user_schemas import (
    LoginSchemas,
    UserModelSchema,
    RegisterSchema,
    UserUpdateSchema,
)
from .user_data import AuthData, AuthResponseData, UserUpdateData

blp = Blueprint(
    "users",
    __name__,
    url_prefix="/user",
    description="""
                user management end point
                """,
)


@blp.route("")
class UserViews(MethodView):
    @jwt_required()
    @blp.arguments(schema=UserUpdateSchema)
    @blp.response(schema=UserModelSchema, status_code=HTTPStatus.CREATED)
    def put(self, user_data: UserUpdateData):

        duplicateUse: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )
        if bool(duplicateUse) == True and duplicateUse.id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message="user name or email already use ",
            )

        userModel = UserModel.update_with_id(
            user_id=getCurrentAuthId(),
            username=user_data.username,
            address=user_data.address,
            description=user_data.description,
            email=user_data.email,
            phone_number=user_data.phone_number,
            occupation=user_data.occupation,
        )
        return userModel


@blp.route("/login")
class UserLoginViews(MethodView):

    @blp.arguments(schema=LoginSchemas)
    @blp.response(schema=UserModelSchema, status_code=HTTPStatus.OK)
    @blp.alt_response(
        status_code=HTTPStatus.FORBIDDEN,
        description="user not found",
    )
    def post(self, user_data: AuthData):

        user: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )
        if user and user.match_password(receive_password=user_data.password):

            access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
            return AuthResponseData(user_model=user, access_token=access_token)

        abort(http_status_code=HTTPStatus.FORBIDDEN, message="Invalid credentials")


@blp.route("/register")
class UserRegisterView(MethodView):
    @blp.arguments(schema=RegisterSchema)
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description="duplicate username",
    )
    def post(self, item_data: AuthData):

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


@blp.route("/sign-in")
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


@blp.route("/image")
class ImageUserViews(MethodView):
    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserModelSchema)
    def post(self, data: ImagesPayloadData):
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data):
            response_data: ImageData = ImageService.image_save(image_data=image_data)
            UserImageModel.add_model(
                public_id=response_data.public_id,
                secure_url=response_data.secure_url,
                user_id=getCurrentAuthId(),
            )

            return UserModel.get_model_by_id(model_id=getCurrentAuthId())
