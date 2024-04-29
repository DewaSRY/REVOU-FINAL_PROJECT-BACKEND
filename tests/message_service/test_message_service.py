"""_summary_
"""

from unittest import TestCase, skip

from pprint import pprint
from app.message_service import MessageService


class TestMessageService(TestCase):
    # @skip("just skip")
    def test_first_test(self):

        assert MessageService.get_message("first_massage") == "hallo"

    def test_formate_message(self):
        pprint(MessageService.get_message("second_massage").format("hallo"))
        assert MessageService.get_message("first_massage") == "hallo"

    # @skip("just skip")
    def test_get_error_message(self):
        message = "first_massage_two"
        try:
            MessageService.get_message(key_name=message)
        except Exception as e:
            assert str(e) == f"message :'{message}' not found"
