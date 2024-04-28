"""_summary_
"""

from dataclasses import dataclass, field
from app.image_upload_service import ImageData


@dataclass
class UserImageData(ImageData):
    user_id: str = field(default_factory=str)

    def __init__(self, public_id: str, secure_url: str, user_id: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.user_id = user_id
