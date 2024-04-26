"""_summary_
"""

from dataclasses import dataclass


@dataclass
class JWTData:
    user_id: str
    is_admin: bool

    def __init__(self, user_id: str, user_type: str):
        self.user_id = user_id
        self.is_admin(user_type=user_type)

    def is_admin(self, user_type: str):
        self.is_admin = user_type == "admin"

    def to_json(self):
        return {"current_id": self.user_id, "is_admin": self.is_admin}
