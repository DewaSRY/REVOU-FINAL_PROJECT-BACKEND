"""_summary_
"""

from .business_blp import blp
from flask_smorest import abort
from flask.views import MethodView
from http import HTTPStatus
from app.final_project_api.model.business import (
    BusinessImageData,
    BusinessImageModel,
    BusinessTypeData,
    BusinessTypeModel,
    BusinessModel,
)
from app.jwt_service import getCurrentAuthId
from flask_jwt_extended import jwt_required
from .business_schemas import (
    BusinessModelSchema,
    QueryBusinessSchema,
    BusinessCreateSchema,
    BusinessSchemas,
)
from .business_data import (
    QueryBusinessData,
    BusinessCreateData,
)


@blp.route("/")
class BusinessViews(MethodView):
    @blp.arguments(schema=QueryBusinessSchema, location="query")
    @blp.response(schema=BusinessSchemas(many=True), status_code=HTTPStatus.OK)
    def get(self, query_args: QueryBusinessData):
        print(query_args)
        return BusinessModel.get_all_model()

    @jwt_required()
    @blp.arguments(schema=BusinessCreateSchema)
    @blp.response(schema=BusinessModelSchema, status_code=HTTPStatus.CREATED)
    def post(self, business_data: BusinessCreateData):
        try:
            model = BusinessModel.add_model(
                user_id=getCurrentAuthId(),
                business_name=business_data.business_name,
                business_type_name=business_data.business_types,
            )
            return model
        except Exception as e:
            abort(http_status_code=HTTPStatus.CONFLICT, message=str(e))
