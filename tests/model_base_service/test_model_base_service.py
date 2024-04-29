"""_summary_
"""

from tests.mock_database_connection import MockDatabaseConnection
from .mock_model import MockModelBase
from .mock_data import MockData
from pprint import pprint
from unittest import skip


class TestModelBaseService(MockDatabaseConnection):
    def setup_class(self):
        super().setup_class(self)
        self.test_name = "some name"
        self.test_model = MockModelBase.add_model(MockModelBase(name=self.test_name))

    def teardown_class(self):
        super().teardown_class(self)
        MockModelBase.clean_all_model()

    # @skip("just skip")
    def test_add_model_by_ModelBaseService(self):
        testing_mock = MockModelBase("hallo")
        MockModelBase.add_model(testing_mock)
        find_match_model = (
            MockModelBase.session.query(MockModelBase)
            .filter(MockModelBase.id == testing_mock.id)
            .first()
        )
        assert testing_mock == find_match_model

    # @skip("just skip")
    def test_create_by_ModelBaseService(self):
        testing_name = "testing"
        MockModelBase.add_model(MockModelBase(name=testing_name))
        testing_model: MockModelBase = (
            MockModelBase.session.query(MockModelBase)
            .filter(MockModelBase.name == testing_name)
            .first()
        )
        # data = MockData(name="some name", username="some user name")
        # pprint( indent=2)

        assert testing_model.name == testing_name

    # @skip("just skip")
    def test_update_by_ModelBaseService(self):
        testing_first_name = "firstName"
        testing_second_name = "second name"
        first_models = MockModelBase.add_model(MockModelBase(name=testing_first_name))
        second_models = MockModelBase.update_model(
            first_models, name=testing_second_name
        )

        assert first_models.id == second_models.id

    # @skip("just skip")
    def test_delete_by_ModelBaseService(self):
        model_to_delete = "model to delete "

        create_model = MockModelBase.add_model(MockModelBase(name=model_to_delete))
        create_model_id = create_model.id
        test_find_model = (
            MockModelBase.session.query(MockModelBase)
            .filter(MockModelBase.id == create_model_id)
            .first()
        )
        assert test_find_model != None

        MockModelBase.delete_model(create_model)
        testing_model = (
            MockModelBase.session.query(MockModelBase)
            .filter(MockModelBase.id == create_model_id)
            .first()
        )

        assert testing_model == None

    # @skip("just skip")
    def test_model_can_delete_all_model(self):
        """test_model_can_delete_all_model"""
        name_list = ["name one", "name two", "name three"]
        model_list: list[MockModelBase] = map(
            lambda name: MockModelBase(name=name), name_list
        )
        MockModelBase.add_all_model(model_list)
        MockModelBase.clean_all_model()
        all_model: list[MockModelBase] = MockModelBase.session.query(
            MockModelBase
        ).all()
        assert len(all_model) == 0

    # @skip("just skip")
    def test_delete_model_by_id(self):
        prev_model_id = self.test_model.id
        MockModelBase.delete_model_with_id(model_id=prev_model_id)
        find_prev_model = MockModelBase.get_model_by_id(model_id=prev_model_id)
        assert find_prev_model == None

    # @skip("just skip")
    def test_update_model_by_id(self):
        prev_model_id = self.test_model.id
        new_model_name = "new name"
        MockModelBase.update_with_id(model_id=prev_model_id, name=new_model_name)

        find_prev_mode: MockModelBase = MockModelBase.get_model_by_id(
            model_id=prev_model_id
        )
        assert find_prev_mode.id == prev_model_id
        assert find_prev_mode.name == new_model_name
        assert find_prev_mode.name != self.test_name
