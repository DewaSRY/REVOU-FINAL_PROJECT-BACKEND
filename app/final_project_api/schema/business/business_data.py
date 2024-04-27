"""_summary_
"""

from dataclasses import dataclass, field


@dataclass
class BusinessCreateData:
    business_name: str
    business_types: str


@dataclass
class QueryBusinessData:
    page: int = field(default_factory=lambda: 1)
    limit: int = field(default_factory=lambda: 10)
