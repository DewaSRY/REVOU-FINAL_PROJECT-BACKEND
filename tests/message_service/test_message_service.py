"""_summary_
"""

from unittest import TestCase

from pprint import pprint
from app.message_service import MassageService


class TestMessageService(TestCase):

    def test_first_test(self):

        assert MassageService.get_message("first_massage") == "hallo"

    def test_get_error_message(self):
        message = "first_massage_two"
        try:
            MassageService.get_message(key_name=message)
        except Exception as e:
            assert str(e) == f"message :'{message}' not found"
