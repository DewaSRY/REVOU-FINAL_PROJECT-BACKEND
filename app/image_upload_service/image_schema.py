"""_summary_

Returns:
    _type_: _description_
"""

from flask import current_app
from marshmallow import (
    Schema,
    fields,
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


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


# class MySchema(Schema):
#     icon_url = fields.Field(
#         metadata={"type": "string", "format": "byte"}, allow_none=True
#     )

#     @validates_schema
#     def validate_uploaded_file(self, in_data, **kwargs):
#         errors = {}
#         file: FileStorage = in_data.get("icon_url", None)

#         if file is None:
#             # if any file is not uploaded, skip validation
#             pass

#         elif type(file) != FileStorage:
#             errors["icon_url"] = [f"Invalid content. Only PNG, JPG/JPEG files accepted"]
#             raise ValidationError(errors)

#         elif file.content_type not in {"image/jpeg", "image/png"}:
#             errors["icon_url"] = [
#                 f"Invalid file_type: {file.content_type}. Only PNG, JPG/JPEG images accepted."
#             ]
#             raise ValidationError(errors)

#         return in_data

#     @post_load
#     def post_load(self, loaded_obj, **kwargs):
#         if loaded_obj.icon_url:
#             sec_filename = secure_filename(
#                 f'{loaded_obj.name}.{loaded_obj.icon_url.filename.split(".")[-1]}'
#             )
#             loaded_obj.icon_url.save(
#                 f"{current_app.config['PUBLIC_IMAGES_FOLDER']}{sec_filename}"
#             )
#             loaded_obj.icon_url = (
#                 f'{current_app.config["PUBLIC_IMAGES_URL"]}{sec_filename}'
#             )
#         return loaded_obj
