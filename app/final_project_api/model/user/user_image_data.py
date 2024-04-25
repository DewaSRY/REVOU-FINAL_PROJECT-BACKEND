"""_summary_
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class UserImageData:
    id: str = field(init=False)
    image_url: str
    user_id: str

    def __init__(self, image_url: str, user_id: str):
        self.id = str(uuid4())
        self.image_url = image_url
        self.user_id = user_id
