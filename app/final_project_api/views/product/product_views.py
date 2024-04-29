"""_summary_
"""

from http import HTTPStatus

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest.fields import Upload

from app.image_upload_service import (
    ImageService,
    ImageSchema,
    ImageData,
    ImagesPayloadData,
)
from app.jwt_service import getCurrentAuthId
from app.message_service import MessageService

from app.final_project_api.model.product import (
    ProductData,
    ProductImageData,
    ProductImageModel,
    ProductModel,
    ProductCreateData,
)
from app.final_project_api.model.business import BusinessModel
from app.final_project_api.model.user import UserModel
from app.final_project_api.util import QuerySchema, QueryData

from .product_schemas import (
    ProductSchema,
    ProductModelSchema,
    ProductPublicSchemas,
    ProductCreateSchema,
    ProductImageModelSchema,
    ProductWithImageModel,
)


blp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    description="""
                user management end point
                """,
)


@blp.route("/")
class ProductViews(MethodView):

    @blp.arguments(schema=QuerySchema, location="query")
    @blp.response(schema=ProductPublicSchemas(many=True), status_code=HTTPStatus.OK)
    def get(self, query_data: QueryData):
        return ProductModel.get_all_public_model(query_data=query_data)

    @jwt_required()
    @blp.arguments(schema=ProductCreateSchema)
    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.CREATED)
    def post(self, product_data: ProductCreateData):
        businessModel: BusinessModel = BusinessModel.get_by_user_id()

        try:
            return ProductModel.add_model(
                business_id=product_data.business_id,
                product_name=product_data.product_name,
                product_price=product_data.product_price,
                description=product_data.description,
            )
        except Exception as e:
            abort(http_status_code=HTTPStatus.CONFLICT, message=str(e))


@blp.route("/<string:product_id>")
class ProductByIdViews(MethodView):

    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.OK)
    def get(self, product_id: id):
        return ProductModel.get_model_by_id(model_id=product_id)

    def put():
        pass

    def delete(self):
        pass


# TODO: handle product  image
@blp.route("/image")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=ProductImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        description=MessageService.get_message("file_not_image_type"),
    )
    def post(self, data: ImagesPayloadData):
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data) != True:
            abort(
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                message=MessageService.get_message("file_not_image_type"),
            )
        response_data: ImageData = ImageService.image_save(image_data=image_data)
        userImageModel = ProductImageModel.add_model(
            public_id=response_data.public_id,
            secure_url=response_data.secure_url,
            user_id=getCurrentAuthId(),
        )
        return userImageModel

    @jwt_required()
    @blp.response(status_code=HTTPStatus.CREATED, schema=ProductWithImageModel)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("account-not-found").format(
            "from jwt token"
        ),
    )
    def get(self):
        userModel: ProductModel = ProductModel.get_model_by_id(
            model_id=getCurrentAuthId()
        )
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
    @blp.response(status_code=HTTPStatus.OK, schema=ProductImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def get(self, image_id: str):
        imageMode: ProductImageModel = ProductImageModel.get_model_by_id(
            model_id=image_id
        )
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        return ProductImageModel.get_model_by_id(model_id=image_id)

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def delete(self, image_id: str):
        imageMode: ProductImageModel = ProductImageModel.get_model_by_id(
            model_id=image_id
        )
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        userImageModel = ProductImageModel.delete_model_by_id(model_id=image_id)
        ImageService.image_delete(public_id=userImageModel.public_id)
        return {"message": f"image with id '{image_id}' delete  success fully"}

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED, schema=ProductWithImageModel)
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
        imageMode: ProductImageModel = ProductImageModel.get_model_by_id(
            model_id=image_id
        )
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        try:
            return ProductImageModel.put_as_profile(image_id=image_id)
        except Exception as e:
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_update_profile").format(
                    image_id
                ),
            )
