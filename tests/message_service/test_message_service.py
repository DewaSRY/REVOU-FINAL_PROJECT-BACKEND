"""_summary_
"""

from unittest import TestCase

from pprint import pprint
from app.message_service import MassageService


class TestMessageService(TestCase):

    def test_first_test(self):

        # pprint(MassageService.gettext("first_massage"))
        # pprint(MassageService.gettext("first_massage"))
        # pprint(MassageService.gettext("first_massage"))
        assert MassageService.gettext("first_massage") == "hallo"
