from dataclasses import dataclass, field
from app.model_base_service import ModelBaseDefault


@dataclass
class UserData(ModelBaseDefault):
    username: str
    password: str
    email: str

    def __init__(self, username: str, email: str, password: str):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self._set_password(password)

    def _set_password(self, password: str):
        raise Exception(f"{self.__class__} not implement _set_password")

    def match_password(self, receive_password: str) -> bool:
        raise Exception(f"{self.__class__} not implement _match_password")

    def create_account(self) -> int:
        """create_account
        method will call when user create some account
        Raises:
            Exception: _description_
        """
        raise Exception(f"{self.__class__} not implement account_get_create")
