"""_summary_
"""

from .image_data import ImageSaveData
from werkzeug.datastructures import FileStorage


class ImageServiceAble:
    def save_image(self, image_data: FileStorage) -> ImageSaveData:
        raise Exception(f"{self.__class__} not implement 'save_image' ")

    def delete_image(self, public_id: str):
        raise Exception(f"{self.__class__} not implement 'delete_image'")
