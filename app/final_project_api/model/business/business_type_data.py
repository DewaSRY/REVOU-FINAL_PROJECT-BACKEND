"""_summary_
"""

from dataclasses import dataclass, field


@dataclass
class BusinessTypeData:
    id: int = field(init=False)
    name: str

    def __init__(self, name: str):
        self.name = name
