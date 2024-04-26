"""_summary_
"""

from dataclasses import dataclass
from app.image_upload_service import ImageData


@dataclass
class UserImageData(ImageData):
    user_id: str

    def __init__(self, image_url: str, user_id: str):
        super().__init__(image_url=image_url)
        self.user_id = user_id
