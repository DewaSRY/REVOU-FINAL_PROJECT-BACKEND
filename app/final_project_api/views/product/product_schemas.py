"""_summary_
"""

from marshmallow import Schema, fields, post_load
from app.final_project_api.model.product import ProductCreateData
from app.image_upload_service import ImageModelSchema


class ProductImageModelSchema(ImageModelSchema):
    product_name = fields.Str()


class ProductSchema(Schema):
    # TODO: delete this and change what inside user schema
    product_name = fields.Str()
    product_price = fields.Float()
    product_images = fields.List(fields.Nested(ImageModelSchema))
    profile_url = fields.Str()
    id = fields.Str()
    description = fields.Str()


class ProductCreateSchema(Schema):
    product_name = fields.Str(required=True)
    product_price = fields.Float(required=True)
    business_id = fields.Str(required=True)
    description = fields.Str(required=True)

    @post_load
    def get_data(self, data, **kwarg):
        return ProductCreateData(**data)


class ProductPublicSchemas(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    profile_url = fields.Str()
    business_name = fields.Str(required=True)
    username = fields.Str(required=True)
    business_id = fields.Str(required=True)
    user_id = fields.Str(required=True)


class PrivateProductSchema(ProductPublicSchemas):
    is_delete = fields.Bool()


class ProductModelSchema(ProductPublicSchemas):
    product_images = fields.List(fields.Nested(ImageModelSchema))


class ProductWithImageModel(Schema):
    product_name = fields.Str()
    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    profile_url = fields.Str()
    product_images = fields.List(fields.Nested(ImageModelSchema))
