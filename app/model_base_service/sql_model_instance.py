"""_summary_
"""

from typing import TypeVar
from .db import db

SQLModelInstance=TypeVar("SQLModelInstance", bound=db.Model)