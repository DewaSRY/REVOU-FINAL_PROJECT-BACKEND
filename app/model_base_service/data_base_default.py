"""_summary_
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class DataBaseDefault:
    """ModelBaseDefault
    will inherit property
        - id
        - update_at
        - create_at
    """

    id: str = field(init=False)
    update_at: datetime = field(init=False)
    create_at: datetime = field(init=False, default_factory=lambda: datetime.now())

    def __init__(self):
        self.id = str(uuid4())
        self.update_at = datetime.now()
        self.create_at = datetime.now()
