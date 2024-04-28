# """_summary_
# """

from dataclasses import dataclass, field
from app.image_upload_service import ImageData


@dataclass
class BusinessImageData(ImageData):
    business_id: str = field(default_factory=str)

    def __init__(self, public_id: str, business_id: str, secure_url: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.business_id = business_id
