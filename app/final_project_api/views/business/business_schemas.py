"""_summary_
"""

from marshmallow import Schema, fields, post_load
from app.final_project_api.views.product.product_schemas import ProductSchema
from .business_data import QueryBusinessData, BusinessCreateData


class QueryBusinessSchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()

    @post_load
    def get_data(self, data, **kwargs):
        return QueryBusinessData(**data)


class BusinessSchemas(Schema):
    business_types = fields.Str()
    business_name = fields.Str()
    profile_url = fields.Str()
    business_images = fields.List(fields.Str())
    id = fields.Str()


class BusinessCreateSchema(Schema):
    business_name = fields.Str(required=True)
    business_types = fields.Str(required=True)

    @post_load
    def create_data(self, data, **kwargs):
        return BusinessCreateData(**data)


class BusinessModelSchema(BusinessSchemas):
    product = fields.List(fields.Nested(ProductSchema), dump_only=True)
