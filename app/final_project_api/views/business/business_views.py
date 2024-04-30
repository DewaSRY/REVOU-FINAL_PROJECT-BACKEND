"""_summary_
"""

from http import HTTPStatus

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest.fields import Upload

from app.final_project_api.model.business import (
    BusinessImageData,
    BusinessImageModel,
    BusinessTypeData,
    BusinessTypeModel,
    BusinessModel,
)
from app.image_upload_service import (
    ImageService,
    ImageSchema,
    ImageData,
    ImagesPayloadData,
)
from app.jwt_service import getCurrentAuthId
from app.message_service import MessageService
from .business_schemas import (
    BusinessModelSchema,
    BusinessCreateSchema,
    BusinessSchemas,
    BusinessCreateData,
    BusinessUpdateSchema,
    BusinessWithImageModel,
    BusinessImageModelSchema,
    BusinessPublicSchema,
)

from app.final_project_api.util import QueryData, QuerySchema
from pprint import pprint

blp = Blueprint(
    "business",
    __name__,
    url_prefix="/api/business",
    description="""
                business management end point
                """,
)


@blp.route("/")
class BusinessViews(MethodView):
    @blp.arguments(schema=QuerySchema, location="query")
    @blp.response(schema=BusinessPublicSchema(many=True), status_code=HTTPStatus.OK)
    def get(self, query_data: QueryData):

        return BusinessModel.get_all_public_model(query_data=query_data)

    @jwt_required()
    @blp.arguments(schema=BusinessCreateSchema)
    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.CREATED)
    @blp.alt_response(
        status_code=HTTPStatus.BAD_REQUEST,
        description=MessageService.get_message("failed_to_add_business").format(
            "pass on payload"
        ),
    )
    def post(self, business_data: BusinessCreateData):
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
        businessModel: BusinessModel = BusinessModel.get_model_by_id(
            model_id=business_id
        )
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
    def put(self, business_data: BusinessCreateData, business_id: str):
        try:
            return BusinessModel.update_by_id(
                business_id=business_id, update_data=business_data
            )
        except Exception as e:
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
    def delete(self, business_id: str):
        try:
            BusinessModel.delete_by_id(model_id=business_id)
            return {"message": f"business with id {business_id} success filly delete"}
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_to_delete_business").format(
                    business_id
                ),
            )


# TODO: handle product  image
@blp.route("/image/<string:product_id>")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=BusinessImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        description=MessageService.get_message("file_not_image_type"),
    )
    def post(self, data: ImagesPayloadData, product_id: str):
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
                product_id=product_id,
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
    def get(self, product_id: str):
        """_summary_
        Args:
            product_id (str): _description_
        Returns:
            _type_: _description_
        """
        userModel: BusinessModel = BusinessModel.get_model_by_id(model_id=product_id)
        if bool(userModel) == False:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=MessageService.get_message("product_not_found").format(
                    product_id
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
    )
    def get(self, product_id: str, image_id: str):
        imageMode: BusinessImageModel = BusinessImageModel.get_model_by_id(
            model_id=image_id
        )
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        return BusinessImageModel.get_model_by_id(model_id=image_id)

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def delete(self, product_id: str, image_id: str):
        imageMode: BusinessImageModel = BusinessImageModel.get_model_by_id(
            model_id=image_id
        )
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
    )
    @blp.alt_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description=MessageService.get_message("failed_update_profile").format(
            "pass on the url string"
        ),
    )
    def put(self, product_id: str, image_id: str):
        imageMode: BusinessImageModel = BusinessImageModel.get_model_by_id(
            model_id=image_id
        )
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
