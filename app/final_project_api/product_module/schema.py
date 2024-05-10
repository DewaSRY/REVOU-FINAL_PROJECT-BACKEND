"""_summary_
"""

from marshmallow import Schema, fields, post_load
from .data import ProductCreateData, ProductUpdateData
from app.image_upload_service import ImageModelSchema
from app.util.query_data import QuerySchema
from flask_marshmallow.fields import Hyperlinks, URLFor


class ProductImageModelSchema(ImageModelSchema):
    product_name = fields.Str()
    product_id = fields.Str()


class ProductSchema(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    profile_url = fields.Str()
    id = fields.Str()
    is_delete = fields.Bool()
    description = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()


class ProductCreateSchema(Schema):
    product_name = fields.Str(required=True)
    product_price = fields.Float(required=True)
    business_id = fields.Str(required=True)
    description = fields.Str(required=True)

    @post_load
    def get_data(self, data, **kwarg):
        return ProductCreateData(**data)


class ProductUpdateSchema(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    description = fields.Str()

    @post_load
    def get_data(self, data, **kwarg):
        return ProductUpdateData(**data)


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
    description = fields.Str()


class PrivateProductSchema(ProductPublicSchemas):
    is_delete = fields.Bool()


class ProductModelSchema(ProductPublicSchemas):
    product_images = fields.List(fields.Nested(ImageModelSchema))
    _links = Hyperlinks(
        {
            "self": {
                "href": URLFor("product.ProductByIdViews", values=dict(id="<id>")),
                "message": "use for get detail, update or delete ",
            },
            "collection": {
                "href": URLFor("product.ProductViews"),
                "message": "use for get detail or crete ",
            },
            "image": {
                "href": URLFor("product.ImageProductViews", values=dict(id="<id>")),
                "message": "use for post image and see detail image ",
            },
        }
    )


class ProductWithImageModel(Schema):
    product_name = fields.Str()
    id = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    profile_url = fields.Str()
    product_images = fields.List(fields.Nested(ImageModelSchema))


class ProductPublicListSchema(QuerySchema):
    data = fields.List(fields.Nested(ProductPublicSchemas))
    total_page = fields.Integer()
    total_data = fields.Integer()
