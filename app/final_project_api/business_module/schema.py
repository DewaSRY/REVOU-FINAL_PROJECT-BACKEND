"""_summary_
"""

from marshmallow import Schema, fields, post_load

from flask_marshmallow.fields import Hyperlinks, URLFor

from app.final_project_api.product_module.schema import ProductSchema

from app.image_upload_service import ImageModelSchema
from app.util.query_data import QuerySchema
from .data import BusinessCreateData


class BusinessImageModelSchema(ImageModelSchema):
    business_name = fields.Str()
    business_id = fields.Str()


class BusinessSchemas(Schema):
    business_types = fields.Str()
    business_name = fields.Str()
    profile_url = fields.Str()

    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    description = fields.Str()
    is_delete = fields.Bool()


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
    """ """

    product = fields.List(fields.Nested(ProductSchema), dump_only=True)
    business_images = fields.List(fields.Nested(ImageModelSchema))

    _links = Hyperlinks(
        {
            "self": {
                "href": URLFor("business.BusinessByIdViews", values=dict(id="<id>")),
                "message": "use for get detail, update or delete ",
            },
            "collection": {
                "href": URLFor("business.BusinessViews"),
                "message": "use for get detail or crete ",
            },
            "image": {
                "href": URLFor("business.ImageBusinessViews", values=dict(id="<id>")),
                "message": "use for post image and see detail image ",
            },
        }
    )


class BusinessWithImageModel(Schema):
    product_name = fields.Str()
    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    profile_url = fields.Str()
    business_images = fields.List(fields.Nested(ImageModelSchema))


class BusinessPublicListSchema(QuerySchema):
    data = fields.List(fields.Nested(BusinessPublicSchema))
    total_page = fields.Integer()
    total_data = fields.Integer()
