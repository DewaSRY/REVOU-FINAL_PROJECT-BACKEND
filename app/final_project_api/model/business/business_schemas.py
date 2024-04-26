"""_summary_
"""

from marshmallow import Schema, fields


class BusinessSchemas(Schema):
    business_types = fields.Str()
    business_name = fields.Str()
    business_images = fields.List(fields.Str())
