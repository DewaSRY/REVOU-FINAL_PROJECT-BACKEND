"""_summary_
"""

from flask.views import MethodView
from .user_blp import blp


from flask_smorest.fields import Upload
from cloudinary.utils import cloudinary_url


from pprint import pprint
from app.image_upload_service import (
    ImageService,
    ImageSchema,
    ImageData,
    ImagesPayloadData,
)


@blp.route("/image")
class ImageUserViews(MethodView):
    @blp.arguments(schema=ImageSchema, location="files")
    def post(self, data: ImagesPayloadData):
        image_data: Upload = data.image
        if ImageService.check_extension(image_data=image_data):
            response_data: ImageData = ImageService.image_save(image_data=image_data)
            pprint(response_data.secure_url, indent=2)

            return {"message": response_data.secure_url}
