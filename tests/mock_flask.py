"""_summary_
"""

from unittest import TestCase
from flask.testing import FlaskClient

from app.final_project_api import create_app


class MockFlask(TestCase):

    def setup_class(self):
        self.app = create_app()
        self.app.config.update(
            {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///tests/data.db"}
        )
        self.client: FlaskClient = self.app.test_client()
