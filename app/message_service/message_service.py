"""_summary_

Returns:
    _type_: _description_
"""

import json
from os import getcwd, path


class MessageService:
    base_dir = basedir = path.join(getcwd(), "app", "message_service")
    default_locale = "en-gb"
    cached_strings = {}
    massage_json_phat = f"{base_dir}/{default_locale}.json"

    @classmethod
    def refresh(cls):
        with open(cls.massage_json_phat) as f:
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
