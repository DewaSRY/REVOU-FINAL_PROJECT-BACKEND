"""_summary_
"""

from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime


@dataclass
class ImageData:
    """ImageData
    - id
    - secure_url
    - public_id,
    create_at: datetime = field(init=False, default_factory=lambda: datetime.now())
    """

    id: str = field(init=False, default_factory=lambda: str(uuid4()))
    secure_url: str = field(default_factory=lambda: "")
    public_id: str = field(default_factory=lambda: str(uuid4()))
    create_at: datetime = field(init=False, default_factory=lambda: datetime.now())


# @dataclass
# class ImageSaveData:
#     public_id: str
#     secure_url: str
