"""_summary_
"""

from marshmallow import Schema, fields, post_load
from dataclasses import dataclass, field


@dataclass
class QueryData:
    page: int = field(default_factory=lambda: 1)
    limit: int = field(default_factory=lambda: 10)


class QuerySchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()

    @post_load
    def get_data(self, data, **kwargs):
        return QueryData(**data)
