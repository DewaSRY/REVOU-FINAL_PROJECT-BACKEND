"""_summary_
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ImageData:
    id: str = field(init=False)
    image_url: str

    def __init__(self, image_url: str):
        self.id = str(uuid4())
        self.image_url = image_url


@dataclass
class ImageSaveData:
    public_id: str
    secure_url: str
