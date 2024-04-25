"""_summary_
"""

from dataclasses import dataclass, field


@dataclass
class UserTypeData:
    id: str = field(init=False)
    name: str
