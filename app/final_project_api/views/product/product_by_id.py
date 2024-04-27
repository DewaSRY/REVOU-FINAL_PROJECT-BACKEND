"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required


from .product_blp import blp
from app.final_project_api.model.product import (
    ProductCreateData,
    ProductCreateSchema,
    ProductData,
    ProductImageData,
    ProductImageModel,
    ProductModel,
    ProductSchema,
    ProductModelSchema,
)


@blp.route("/product/<string:product_id>")
class ProductByIdViews(MethodView):

    @blp.response(schema=ProductModelSchema, status_code=HTTPStatus.OK)
    def get(self, product_id: id):
        return ProductModel.get_model_by_id(model_id=product_id)

    # @jwt_required
    # @blp.arguments(schema=ProductCreateSchema)
    # def post(self, product_data: ProductCreateData):
    #     try:
    #         return ProductModel.add_model(
    #             business_id=product_data.business_id,
    #             product_name=product_data.product_name,
    #             product_price=product_data.product_price,
    #         )
    #     except Exception as e:
    #         abort(http_status_code=HTTPStatus.CONFLICT, message=str(e))
