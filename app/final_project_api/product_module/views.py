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

from .data import ProductCreateData
from .image_model import ProductImageModel
from .model import ProductModel, ProductUpdateData
from app.final_project_api.business_module.model import BusinessModel
from app.final_project_api.user_module.model import UserModel
from app.util import QuerySchema, QueryData

from .schema import (
    ProductModelSchema,
    ProductPublicSchemas,
    ProductCreateSchema,
    ProductImageModelSchema,
    ProductWithImageModel,
    ProductUpdateSchema,
)


blp = Blueprint(
    "product",
    __name__,
    url_prefix="/api/product",
    description="manage product user product ",
)


@blp.route("")
class ProductViews(MethodView):

    @blp.arguments(schema=QuerySchema, location="query")
    @blp.response(schema=ProductPublicSchemas(many=True), status_code=HTTPStatus.OK)
    def get(self, query_data: QueryData):
        """As a user, i can get all product event without access token"""
        return ProductModel.get_all_public(query_data=query_data)

    @jwt_required()
    @blp.arguments(schema=ProductCreateSchema)
    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.CREATED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("business-not-found").format(
            "on data payload"
        ),
    )
    @blp.alt_response(
        status_code=HTTPStatus.NOT_ACCEPTABLE,
        description=MessageService.get_message("user_id_on_business_not_match").format(
            "on data payload"
        ),
    )
    def post(self, product_data: ProductCreateData):
        """As a user, i can create product"""
        businessModel: BusinessModel = BusinessModel.get_by_id(
            model_id=product_data.business_id
        )
        if bool(businessModel) == False or businessModel.user_id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("business-not-found").format(
                    product_data.business_id
                ),
            )
        if businessModel.user_id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.NOT_ACCEPTABLE,
                message=MessageService.get_message(
                    "user_id_on_business_not_match"
                ).format(businessModel.id),
            )
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
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("product_not_found").format(
            "pass ont url"
        ),
    )
    @jwt_required()
    def get(self, product_id: str):
        """as a user i can get my product by its id"""
        productModel: ProductModel = ProductModel.get_by_id(model_id=product_id)
        if bool(productModel) == False or (
            productModel.delete_model == True
            or productModel.user_id != getCurrentAuthId()
        ):
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("product_not_found").format(
                    product_id
                ),
            )

        return productModel

    @jwt_required()
    @blp.arguments(schema=ProductUpdateSchema)
    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.CREATED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_ACCEPTABLE,
        description=MessageService.get_message("user_id_on_product_not_match").format(
            "on url string"
        ),
    )
    def put(self, product_data: ProductUpdateData, product_id: str):
        """As a user,i can update my product by its id"""
        productModel: ProductModel = ProductModel.get_by_id(model_id=product_id)
        if productModel.user_id != getCurrentAuthId():
            abort(
                http_status_code=HTTPStatus.NOT_ACCEPTABLE,
                message=MessageService.get_message(
                    "user_id_on_product_not_match"
                ).format(product_id),
            )
        try:
            return ProductModel.update_with_update_data(
                product_id=product_id, product_data=product_data
            )
        except Exception as e:
            abort(http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

    @jwt_required()
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("product_not_found").format(
            "pass ont url"
        ),
    )
    def delete(self, product_id: str):
        """As a user, i can delete my product by its id"""
        try:
            deleteModel: ProductModel = ProductModel.delete_model_by_id(
                model_id=product_id
            )
            if bool(deleteModel) == False:
                abort(
                    http_status_code=HTTPStatus.NOT_FOUND,
                    message=MessageService.get_message("product_not_found").format(
                        product_id
                    ),
                )
            return {"message": f"product with id '{product_id}' success full delete"}
        except Exception as e:
            print(str(e))
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=f"failed to delete product with id '{product_id}' ",
            )


@blp.route("/image/<string:product_id>")
class ImageUserViews(MethodView):

    @jwt_required()
    @blp.arguments(schema=ImageSchema, location="files")
    @blp.response(status_code=HTTPStatus.CREATED, schema=ProductImageModelSchema)
    @blp.alt_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        description=MessageService.get_message("file_not_image_type"),
    )
    def post(self, data: ImagesPayloadData, product_id: str):
        """As a user, i can post image to my product"""
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data) != True:
            abort(
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                message=MessageService.get_message("file_not_image_type"),
            )
        response_data: ImageData = ImageService.image_save(image_data=image_data)
        try:
            userImageModel = ProductImageModel.add_model(
                public_id=response_data.public_id,
                secure_url=response_data.secure_url,
                product_id=product_id,
            )
            return userImageModel
        except Exception as e:
            ImageService.image_delete(public_id=response_data.public_id)
            abort(http_status_code=HTTPStatus.NOT_FOUND, message=str(e))

    @jwt_required()
    @blp.response(status_code=HTTPStatus.CREATED, schema=ProductWithImageModel)
    @blp.alt_response(
        status_code=HTTPStatus.CONFLICT,
        description=MessageService.get_message("account-not-found").format(
            "from jwt token"
        ),
    )
    def get(self, product_id: str):
        """As a user, i can get image by its id"""
        userModel: ProductModel = ProductModel.get_by_id(model_id=product_id)
        if bool(userModel) == False:
            abort(
                http_status_code=HTTPStatus.CONFLICT,
                message=MessageService.get_message("product_not_found").format(
                    product_id
                ),
            )
        return userModel


@blp.route("/product-image/<string:image_id>")
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
        """As a user, i can get image by its id"""
        imageMode: ProductImageModel = ProductImageModel.get_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        return ProductImageModel.get_by_id(model_id=image_id)

    @jwt_required()
    @blp.response(status_code=HTTPStatus.ACCEPTED)
    @blp.alt_response(
        status_code=HTTPStatus.NOT_FOUND,
        description=MessageService.get_message("image_not_found").format(
            "pass on url string"
        ),
    )
    def delete(self, image_id: str):
        """As a user, i can delete image by its id"""
        imageMode: ProductImageModel = ProductImageModel.get_by_id(model_id=image_id)
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
        """As a user i can put image by its id to the product profile"""
        imageMode: ProductImageModel = ProductImageModel.get_by_id(model_id=image_id)
        if bool(imageMode) == False:
            abort(
                http_status_code=HTTPStatus.NOT_FOUND,
                message=MessageService.get_message("image_not_found").format(image_id),
            )
        try:
            return ProductImageModel.put_as_profile(image_id=image_id)
        except Exception as e:
            print(e)
            abort(
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=MessageService.get_message("failed_update_profile").format(
                    image_id
                ),
            )
