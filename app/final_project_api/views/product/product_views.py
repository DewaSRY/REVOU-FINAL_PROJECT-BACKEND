"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required


from app.final_project_api.model.product import (
    ProductData,
    ProductImageData,
    ProductImageModel,
    ProductModel,
)
from .product_blp import blp

from .product_schemas import (
    ProductSchema,
    ProductModelSchema,
    ProductPublicSchemas,
    ProductCreateSchema,
)

from .product_data import (
    ProductCreateData,
)


@blp.route("/")
class ProductViews(MethodView):

    @blp.response(schema=ProductPublicSchemas(many=True), status_code=HTTPStatus.OK)
    def get(self):
        return ProductModel.get_all_model()

    # @jwt_required()
    @blp.arguments(schema=ProductCreateSchema)
    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.CREATED)
    def post(self, product_data: ProductCreateData):
        try:
            return ProductModel.add_model(
                business_id=product_data.business_id,
                product_name=product_data.product_name,
                product_price=product_data.product_price,
            )
        except Exception as e:
            abort(http_status_code=HTTPStatus.CONFLICT, message=str(e))
