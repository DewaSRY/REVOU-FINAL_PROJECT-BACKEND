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
    def gettext(cls, name: str):
        if bool(cls.cached_strings) != True:
            cls.refresh()

        return cls.cached_strings[name]
