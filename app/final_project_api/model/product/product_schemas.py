from marshmallow import Schema, fields


class ProductSchema(Schema):
    product_name = fields.Str()
    product_price = fields.Float()
    product_images = fields.List(fields.Str())
    id = fields.Str()
