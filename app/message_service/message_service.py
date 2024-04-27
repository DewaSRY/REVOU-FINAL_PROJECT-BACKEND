"""_summary_

Returns:
    _type_: _description_
"""

import json
from os import getcwd, path


class MassageService:
    base_dir = basedir = path.join(getcwd(), "app", "message_service")
    default_locale = "en-gb"
    cached_strings = {}

    @classmethod
    def refresh(cls):
        with open(f"{cls.base_dir}/{cls.default_locale}.json") as f:
            cls.cached_strings = json.load(f)

    @classmethod
    def get_message(cls, key_name: str):
        if bool(cls.cached_strings) != True:
            cls.refresh()
        message: str
        try:
            message = cls.cached_strings[key_name]
        except Exception as e:
            raise Exception(f"message :'{key_name}' not found")
        return message
