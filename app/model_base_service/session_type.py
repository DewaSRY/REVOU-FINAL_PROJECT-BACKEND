from sqlalchemy.orm.session import Session
from typing import TypeVar

SESSION_TYPE=TypeVar("SESSION_TYPE", bound=Session)