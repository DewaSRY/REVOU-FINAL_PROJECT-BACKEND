"""_summary_
"""

from flask_smorest import abort
from flask.views import MethodView
from .image_blp import blp


# import os.path
#
# from flask_smorest.fields import Upload

# from app.image_upload_service import ImageSchema, ImageService
import os.path
from werkzeug.utils import secure_filename
from flask_smorest.fields import Upload
from marshmallow import Schema
from flask import redirect
import os


class MultipartFileSchema(Schema):
    image = Upload()


@blp.route("/image")
class ImageUserViews(MethodView):
    @blp.arguments(schema=MultipartFileSchema, location="files")
    def post(self, data):
        print(data)
        image_data: Upload = data["image"]
        extention = os.path.splitext(image_data.filename)
        image_data.save(os.path.join("upload", secure_filename(image_data.filename)))

        return redirect("/")
