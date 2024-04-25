"""_summary_

Returns:
    _type_: _description_
"""
import json


class MassageService:
    default_locale = "en-gb"
    cached_strings = {}
    @classmethod
    def refresh(cls):
        print("Refreshing...")
        global cached_strings
        with open(f"strings/{cls.default_locale}.json") as f:
            cached_strings = json.load(f)

    def gettext(name):
        
        return cached_strings[name]

