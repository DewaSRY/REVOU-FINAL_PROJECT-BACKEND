"""_summary_
"""

from marshmallow import Schema, fields, post_load
from dataclasses import dataclass, field
from app.final_project_api.model.product import ProductSchema


class BusinessSchemas(Schema):
    business_types = fields.Str()
    business_name = fields.Str()
    business_images = fields.List(fields.Str())
    id = fields.Str()


@dataclass
class BusinessCreateData:
    business_name: str
    business_types: str


class BusinessCreateSchema(Schema):
    business_name = fields.Str(required=True)
    business_types = fields.Str(required=True)

    @post_load
    def create_data(self, data, **kwargs):
        return BusinessCreateData(**data)


class BusinessModelSchema(BusinessSchemas):
    product = fields.List(fields.Nested(ProductSchema), dump_only=True)
