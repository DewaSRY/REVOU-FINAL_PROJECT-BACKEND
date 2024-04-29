"""_summary_

Returns:
    _type_: _description_
"""

from dataclasses import dataclass
from marshmallow import Schema, fields, post_load
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


@dataclass
class ImagesPayloadData:
    image: FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {"invalid": "Not a valid image."}

    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return None
        if not isinstance(value, FileStorage):
            self.fail("invalid")
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)

    @post_load
    def get_data(self, data, **kwargs):
        return ImagesPayloadData(**data)


class ImageModelSchema(Schema):
    id = fields.Str()
    public_id = fields.Str()
    secure_url = fields.Str()
    user_id = fields.Str()
    create_at = fields.DateTime()
