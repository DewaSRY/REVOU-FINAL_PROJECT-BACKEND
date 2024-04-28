"""_summary_
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ImageData:
    secure_url: str = field(default_factory=lambda: "")
    public_id: str = field(default_factory=lambda: str(uuid4()))


# @dataclass
# class ImageSaveData:
#     public_id: str
#     secure_url: str
