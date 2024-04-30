"""_summary_
"""

from marshmallow import Schema, fields, post_load
from app.final_project_api.views.product.product_schemas import ProductSchema
from app.final_project_api.model.business import BusinessCreateData
from app.image_upload_service import ImageModelSchema


class BusinessImageModelSchema(ImageModelSchema):
    business_name = fields.Str()


class BusinessSchemas(Schema):
    business_types = fields.Str()
    business_name = fields.Str()
    profile_url = fields.Str()

    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    description = fields.Str()


class BusinessUpdateSchema(Schema):
    business_name = fields.Str()
    business_types = fields.Str()
    description = fields.Str()

    @post_load
    def create_data(self, data, **kwargs):
        return BusinessCreateData(**data)


class BusinessCreateSchema(Schema):
    business_name = fields.Str(required=True)
    business_types = fields.Str(required=True)
    description = fields.Str(required=True)

    @post_load
    def create_data(self, data, **kwargs):
        return BusinessCreateData(**data)


class BusinessPublicSchema(BusinessSchemas):
    user_phone_number = fields.Str()
    user_email = fields.Str()
    username = fields.Str()


class BusinessModelSchema(BusinessPublicSchema):
    product = fields.List(fields.Nested(ProductSchema), dump_only=True)
    business_images = fields.List(fields.Nested(ImageModelSchema))


class BusinessWithImageModel(Schema):
    product_name = fields.Str()
    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    profile_url = fields.Str()
    business_images = fields.List(fields.Nested(ImageModelSchema))
