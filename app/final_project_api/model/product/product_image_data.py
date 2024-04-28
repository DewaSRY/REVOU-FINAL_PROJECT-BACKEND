# """_summary_
# """

from dataclasses import dataclass, field
from app.image_upload_service import ImageData


@dataclass
class ProductImageData(ImageData):
    product_id: str = field(default_factory=str)

    def __init__(self, public_id: str, product_id: str, secure_url: str):
        super().__init__(public_id=public_id, secure_url=secure_url)
        self.product_id = product_id
