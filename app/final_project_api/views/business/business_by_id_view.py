"""_summary_
"""

from .business_blp import blp
from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus
from app.final_project_api.model.business import (
    BusinessImageData,
    BusinessImageModel,
    BusinessSchemas,
    BusinessTypeData,
    BusinessTypeModel,
    BusinessCreateData,
    BusinessCreateSchema,
    BusinessModel,
    BusinessModelSchema,
)
from app.jwt_service import getCurrentAuthId
from flask_jwt_extended import jwt_required


@blp.route("/business/<string:business_id>")
class BusinessByIdViews(MethodView):

    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.OK)
    def get(self, business_id: str):
        model = BusinessModel.get_model_by_id(model_id=business_id)
        if model == None:
            abort(http_status_code=HTTPStatus.NOT_FOUND, message="business not found")
        return model

    # @jwt_required()
    # @blp.arguments(schema=BusinessCreateSchema)
    # @blp.response(schema=BusinessSchemas, status_code=HTTPStatus.CREATED)
    # def post(self, business_data: BusinessCreateData):
    #     try:
    #         model = BusinessModel.add_model(
    #             user_id=getCurrentAuthId(),
    #             business_name=business_data.business_name,
    #             business_type_name=business_data.business_types,
    #         )
    #         return model
    #     except Exception as e:
    #         abort(http_status_code=HTTPStatus.CONFLICT, message=str(e))
