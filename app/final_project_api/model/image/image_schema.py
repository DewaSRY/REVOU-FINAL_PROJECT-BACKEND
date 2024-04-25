from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        """_deserialize
        Args:
            value (_type_): image receive
            attr (_type_): _description_
            data (_type_): _description_
        Returns:
            FileStorage: _description_
        """
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")
            
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)