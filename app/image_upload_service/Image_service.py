"""_summary_

Returns:
    _type_: _description_
"""

from werkzeug.datastructures import FileStorage

from .image_service_able import ImageServiceAble

from .cloudinary_service import CloudinaryService
from os import path


class ImageService:

    image_service: ImageServiceAble = CloudinaryService()

    image_extension = [".jpeg", ".png", ".gif", ".jpg"]

    @classmethod
    def image_save(cls, image_data: FileStorage):
        return cls.image_service.save_image(image_data=image_data)

    @classmethod
    def image_delete(cls, public_id: str):
        return cls.image_service.delete_image(public_id=public_id)

    @classmethod
    def check_extension(cls, image_data: FileStorage) -> bool:
        extension = path.splitext(image_data.filename)
        return extension[1] in cls.image_extension
