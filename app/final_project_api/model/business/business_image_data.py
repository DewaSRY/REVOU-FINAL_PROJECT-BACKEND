# """_summary_
# """

from dataclasses import dataclass
from app.image_upload_service import ImageData


@dataclass
class BusinessImageData(ImageData):
    business_id: str

    def __init__(self, image_url: str, business_id: str):
        super().__init__()
        self.business_id = business_id
