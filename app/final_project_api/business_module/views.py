"""_summary_
"""

from http import HTTPStatus

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest.fields import Upload


from .type_model import BusinessTypeModel
from .model import BusinessModel
from .image_model import BusinessImageModel
from app.image_upload_service import (
    ImageService,
    ImageSchema,
    ImageData,
    ImagesPayloadData,
)
from app.jwt_service import getCurrentAuthId
from app.message_service import MessageService
from .schema import (
    BusinessModelSchema,
    BusinessCreateSchema,
    BusinessCreateData,
    BusinessUpdateSchema,
    BusinessWithImageModel,
    BusinessImageModelSchema,
    BusinessPublicSchema,
)

from app.util import QueryData, QuerySchema
from pprint import pprint

blp = Blueprint(
    "business",
    __name__,
    url_prefix="/api/business",
    description="business rout use to manage user business data ",
)


@blp.route("")
class BusinessViews(MethodView):
    @blp.arguments(schema=QuerySchema, location="query")
    @blp.response(schema=BusinessPublicSchema(many=True), status_code=HTTPStatus.OK)
    def get(self, query_data: QueryData):
        """As a user, i can get all business public data without auth"""
        return BusinessModel.get_all_public(query_data=query_data)

    @jwt_required()
    @blp.arguments(schema=BusinessCreateSchema)
    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.CREATED)
    @blp.alt_response(
        status_code=HTTPStatus.BAD_REQUEST,
        description=MessageService.get_message("failed_to_add_business").format(
            "pass on payload"
        ),
        example=MessageService.get_message("failed_to_create_business_example"),
    )
    def post(self, business_data: BusinessCreateData):
        """As a auth user, i can create my business"""
        try:
            model = BusinessModel.add_model(
                user_id=getCurrentAuthId(),
                business_name=business_data.business_name,
                business_type_name=business_data.business_types,
                description=business_data.description,
            )
            return model
        except Exception as e:
            message = MessageService.get_message("business_typ_not_found").format(
                f"{business_data.business_types} not in available list: {BusinessTypeModel.get_available_type()}  "
            )
            abort(
                http_status_code=HTTPStatus.BAD_REQUEST,
                message=message,
            )


@blp.route("/<string:business_id>")
class BusinessByIdViews(MethodView):

    @jwt_required()
    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.OK)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("business_not_found").format(
            "pass on url"
        ),
    )
    def get(self, business_id: str):
        """As a user i can get business detail by it's id"""
        businessModel: BusinessModel = BusinessModel.get_by_id(model_id=business_id)
        if (
            bool(businessModel) == False
            or businessModel.is_delete == True
            or businessModel.user_id != getCurrentAuthId()
        ):
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("business_not_found").format(
                    business_id
                ),
            )
        return businessModel

    @jwt_required()
    @blp.arguments(schema=BusinessUpdateSchema)
    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.OK)
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_to_update_business").format(
            "pass on url "
        ),
    )
    @blp.alt_response(
        status_code=HTTPStatus.FORBIDDEN,
        description=MessageService.get_message("failed_to_update_business").format(
            "on url, it might be because user id on business not match with auth user id"
        ),
    )
    def put(self, business_data: BusinessCreateData, business_id: str):
        """As a user i can update my own business data"""
        businessModel: BusinessModel = BusinessModel.get_by_id(model_id=business_id)
        if businessModel.user_id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.FORBIDDEN,
                message=MessageService.get_message("failed_to_delete_business").format(
                    f"{business_id}, business user id not match with auth user id"
                ),
            )
        try:
            return BusinessModel.update_by_id(
                business_id=business_id, update_data=business_data
            )
        except Exception as e:
            print(e)
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_to_update_business").format(
                    business_id
                ),
            )

    @jwt_required()
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_to_delete_business").format(
            "pass on url"
        ),
    )
    @blp.alt_response(
        status_code=HTTPStatus.FORBIDDEN,
        description=MessageService.get_message("failed_to_update_business").format(
            "on url, it might be because user id on business not match with auth user id"
        ),
    )
    def delete(self, business_id: str):
        """As a user i, can delete my own business"""
        businessModel: BusinessModel = BusinessModel.get_by_id(model_id=business_id)
        if businessModel.user_id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.FORBIDDEN,
                message=MessageService.get_message("failed_to_delete_business").format(
                    f"{business_id}, business user id not match with auth user id"
                ),
            )
        try:
            BusinessModel.delete_by_id(model_id=business_id)
            return {"message": f"business with id {business_id} success fully delete"}
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_to_delete_business").format(
                    business_id
                ),
            )


# TODO: handle product  image
@blp.route("/image/<string:business_id>")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=BusinessImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        description=MessageService.get_message("file_not_image_type"),
    )
    def post(self, data: ImagesPayloadData, business_id: str):
        """As a user, i can post business image"""
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data) != True:
            abort(
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                message=MessageService.get_message("file_not_image_type"),
            )
        response_data: ImageData = ImageService.image_save(image_data=image_data)
        try:
            userImageModel = BusinessImageModel.add_model(
                public_id=response_data.public_id,
                secure_url=response_data.secure_url,
                business_id=business_id,
            )
            return userImageModel
        except Exception as e:
            ImageService.image_delete(public_id=response_data.public_id)
            abort(http_status_code=HTTPStatus.NOT_FOUND, message=str(e))

    @jwt_required()
    @blp.response(status_code=HTTPStatus.CREATED, schema=BusinessWithImageModel)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("account-not-found").format(
            "from jwt token"
        ),
    )
    def get(self, business_id: str):
        """As a user, i can see all of my image"""
        userModel: BusinessModel = BusinessModel.get_by_id(model_id=business_id)
        if bool(userModel) == False:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=MessageService.get_message("product_not_found").format(
                    business_id
                ),
            )
        return userModel


@blp.route("/business-image/<string:image_id>")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.response(status_code=HTTPStatus.OK, schema=BusinessImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
        example=MessageService.get_message("image_not_found_example"),
    )
    def get(self, image_id: str):
        """As a user, i can see my image by its id"""
        imageMode: BusinessImageModel = BusinessImageModel.get_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        return BusinessImageModel.get_by_id(model_id=image_id)

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
        example=MessageService.get_message("image_not_found_example"),
    )
    def delete(self, image_id: str):
        """As a user, i can delete my business image"""
        imageMode: BusinessImageModel = BusinessImageModel.get_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        userImageModel = BusinessImageModel.delete_model_by_id(model_id=image_id)
        ImageService.image_delete(public_id=userImageModel.public_id)
        return {"message": f"image with id '{image_id}' delete  success fully"}

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED, schema=BusinessWithImageModel)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
        example=MessageService.get_message("image_not_found_example"),
    )
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_update_profile").format(
            "pass on the url string"
        ),
    )
    def put(self, image_id: str):
        """as a user, i can update my business image"""
        imageMode: BusinessImageModel = BusinessImageModel.get_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        try:
            return BusinessImageModel.put_as_profile(image_id=image_id)
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_update_profile").format(
                    image_id
                ),
            )
