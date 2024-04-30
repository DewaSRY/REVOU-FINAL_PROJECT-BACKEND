"""_summary_
"""

from cloudinary.utils import cloudinary_url
from http import HTTPStatus

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_smorest.fields import Upload
from flask_jwt_extended import jwt_required

from app.final_project_api.model.user import (
    UserModel,
    UserImageModel,
    AuthData,
    UserUpdateData,
    AuthResponseData,
)
from app.jwt_service import createAccessToken, getCurrentAuthId
from app.message_service import MessageService
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
    UserAuthSchema,
    UserImageModelSchema,
    UserWithImagesSchema,
)

blp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/user",
    description="user rout end point, most of it is user account setting from the personal data to the list of personal ownership",
)


@blp.route("/register")
class UserRegisterView(MethodView):
    @blp.arguments(schema=RegisterSchema)
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserAuthSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("duplicate-error").format(
            "data from payload it might be username or email"
        ),
        example=MessageService.get_message("account_data_already_user"),
    )
    def post(self, user_data: AuthData):
        """As a user, i can create an account"""
        userDuplicate: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )
        if bool(userDuplicate):
            duplicate_data: str = (
                user_data.username
                if userDuplicate.username == user_data.username
                else user_data.email
            )
            message = MessageService.get_message("duplicate-error").format(
                duplicate_data
            )
            abort(http_status_code=HTTPStatus.CONFLICT, message=message)

        user = UserModel.add_model(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )
        access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
        return AuthResponseData(user_model=user, access_token=access_token)


@blp.route("/login")
class UserLoginViews(MethodView):

    @blp.arguments(schema=LoginSchemas)
    @blp.response(schema=UserAuthSchema, status_code=HTTPStatus.OK)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("account-not-found").format(
            "username or email not found get send"
        ),
        example=MessageService.get_message("account_not_found_example"),
    )
    @blp.alt_response(
        status_code=HTTPStatus.FORBIDDEN,
        description=MessageService.get_message("password-not-match"),
        example=MessageService.get_message("password_not_match_example"),
    )
    def post(self, user_data: AuthData):
        """As a user, i can login to my registered account"""
        user: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )
        if bool(user) != True:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("account-not-found").format(
                    user_data.getCredential()
                ),
            )

        if user.match_password(receive_password=user_data.password) != True:
            abort(
                http_status_code=HTTPStatus.FORBIDDEN,
                message=MessageService.get_message("password-not-match").format(
                    user_data.passwordNotMatchMessage()
                ),
            )

        access_token = createAccessToken(user_id=user.id, user_type=user.user_type)
        return AuthResponseData(user_model=user, access_token=access_token)


@blp.route("/sign-in")
class UserSignInView(MethodView):

    @jwt_required()
    @blp.response(status_code=HTTPStatus.OK, schema=UserModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("account-not-found").format(
            "from jwt token"
        ),
    )
    def get(self):
        """As a user , i can refresh my data by only provide my access token"""
        userModel = UserModel.get_model_by_id(model_id=getCurrentAuthId())
        if bool(userModel) == False:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=MessageService.get_message("account-not-found").format(
                    getCurrentAuthId()
                ),
            )
        return userModel


@blp.route("")
class UserViews(MethodView):
    @jwt_required()
    @blp.arguments(schema=UserUpdateSchema)
    @blp.response(schema=UserModelSchema, status_code=HTTPStatus.CREATED)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("duplicate-error").format(
            "data from payload"
        ),
        example=MessageService.get_message("account_data_already_user"),
    )
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_update").format(
            "from jwt token"
        ),
    )
    def put(self, user_data: UserUpdateData):
        """As a user, i can update my data registered data"""

        duplicateUse: UserModel = UserModel.get_by_email_or_username(
            username=user_data.username, email=user_data.email
        )

        if bool(duplicateUse) == True and duplicateUse.id != getCurrentAuthId():
            duplicate_data: str = (
                user_data.username
                if duplicateUse.username == user_data.username
                else user_data.email
            )
            message = MessageService.get_message("duplicate-error").format(
                duplicate_data
            )
            abort(http_status_code=HTTPStatus.CONFLICT, message=message)
        try:
            userModel = UserModel.update_with_update_data(
                user_id=getCurrentAuthId(), update_data=user_data
            )
            return userModel
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_update").format(
                    getCurrentAuthId()
                ),
            )


@blp.route("/image")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        description=MessageService.get_message("file_not_image_type"),
        example=MessageService.get_message("not_image_type_error_example"),
    )
    def post(self, data: ImagesPayloadData):
        """as a user, i can post image on the app"""
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data) != True:
            abort(
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                message=MessageService.get_message("file_not_image_type"),
            )
        response_data: ImageData = ImageService.image_save(image_data=image_data)
        userImageModel = UserImageModel.add_model(
            public_id=response_data.public_id,
            secure_url=response_data.secure_url,
            user_id=getCurrentAuthId(),
        )
        return userImageModel

    @jwt_required()
    @blp.response(status_code=HTTPStatus.CREATED, schema=UserWithImagesSchema)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("account-not-found").format(
            "from jwt token"
        ),
    )
    def get(self):
        """As a user, i can see all of my image"""
        userModel: UserModel = UserModel.get_model_by_id(model_id=getCurrentAuthId())
        if bool(userModel) == False:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=MessageService.get_message("account-not-found").format(
                    getCurrentAuthId()
                ),
            )
        return userModel


@blp.route("/image/<string:image_id>")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.response(status_code=HTTPStatus.OK, schema=UserImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def get(self, image_id: str):
        """As a user, i can get my image by its id"""
        imageMode: UserImageModel = UserImageModel.get_model_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        return UserImageModel.get_model_by_id(model_id=image_id)

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def delete(self, image_id: str):
        """As a user, i can delete my image"""
        imageMode: UserImageModel = UserImageModel.get_model_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        userImageModel = UserImageModel.delete_model_by_id(model_id=image_id)
        ImageService.image_delete(public_id=userImageModel.public_id)
        return {"message": f"image with id '{image_id}' delete  success fully"}

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED, schema=UserWithImagesSchema)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_update_profile").format(
            "pass on the url string"
        ),
    )
    def put(self, image_id: str):
        """As a uer, i can change my profile base on my own store image"""
        imageMode: UserImageModel = UserImageModel.get_model_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        try:
            return UserImageModel.put_as_profile(image_id=image_id)
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_update_profile").format(
                    image_id
                ),
            )
