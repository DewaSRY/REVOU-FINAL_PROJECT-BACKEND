# """_summary_
# """

from dataclasses import dataclass
from app.image_upload_service import ImageData


@dataclass
class ProductImageData(ImageData):
    product_id: str

    def __init__(self, image_url: str, product_id: str):
        super().__init__(image_url=image_url)
        self.product_id = product_id
