"""_summary_
"""

from marshmallow import Schema, fields, post_load
from .product_data import ProductCreateData


class ProductSchema(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    product_images = fields.List(fields.Str())
    profile_url = fields.Str()
    id = fields.Str()


class ProductCreateSchema(Schema):
    product_name = fields.Str(required=True)
    product_price = fields.Float(required=True)
    business_id = fields.Str(required=True)

    @post_load
    def get_data(self, data, **kwarg):
        return ProductCreateData(**data)


class ProductPublicSchemas(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    id = fields.Str()
    business_name = fields.Str(required=True)
    username = fields.Str(required=True)
    business_id = fields.Str(required=True)
    user_id = fields.Str(required=True)


class ProductModelSchema(ProductPublicSchemas):
    product_images = fields.List(fields.Str())
