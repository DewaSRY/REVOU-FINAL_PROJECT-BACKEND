"""_summary_
"""

from marshmallow import Schema, fields, post_load
from dataclasses import dataclass, field


@dataclass
class QueryData:
    page: int = field(default_factory=lambda: 1)
    limit: int = field(default_factory=lambda: 10)
    search: str = field(default_factory=str)

    def getSearch(self):
        return f"%{self.search}%"


class QuerySchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()
    search = fields.Str()

    @post_load
    def get_data(self, data, **kwargs):
        return QueryData(**data)
