"""_summary_

Returns:
    _type_: _description_
"""

from cloudinary.uploader import upload
from cloudinary.api import delete_resources

from .image_data import ImageData
from werkzeug.datastructures import FileStorage
from .image_service_able import ImageServiceAble


class CloudinaryService(ImageServiceAble):

    def save_image(self, image_data: FileStorage) -> ImageData:
        uploaded_file = upload(
            unique_filename=False,
            file=image_data,
            folder="final_project",
            public_id="",
        )
        return ImageData(
            public_id=uploaded_file["public_id"], secure_url=uploaded_file["secure_url"]
        )

    def delete_image(self, public_id: str):
        public_ids = [public_id]
        image_delete_result = delete_resources(
            public_ids, resource_type="image", type="upload"
        )
