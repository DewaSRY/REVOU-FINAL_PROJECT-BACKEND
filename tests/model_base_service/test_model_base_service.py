"""_summary_
"""
from tests.mock_database_connection import MockDatabaseConnection
from .mock_model import MockModelBase


class TestModelBaseService(MockDatabaseConnection): 
    def teardown_class(self):
        super().teardown_class(self)
        MockModelBase.clean_all_model()
    def test_add_model_by_ModelBaseService(self):
        testing_mock=MockModelBase("hallo")
        MockModelBase.add_model(testing_mock)
        find_match_model= MockModelBase\
            .session.query(MockModelBase)\
            .filter(MockModelBase.id == testing_mock.id)\
            .first()
        assert testing_mock ==find_match_model
    
    def test_create_by_ModelBaseService(self):
        testing_name="testing"
        MockModelBase.add_model(
            MockModelBase(
                name=testing_name
            )
        )
        testing_model=MockModelBase\
            .session\
            .query(MockModelBase)\
            .filter(MockModelBase.name== testing_name)\
            .first()
        assert testing_model.name== testing_name
        
    def test_update_by_ModelBaseService(self):
        testing_first_name="firstName"
        testing_second_name="second name"
        first_models=MockModelBase\
            .add_model(MockModelBase(name= testing_first_name))
        second_models= MockModelBase\
            .update_model(first_models, name= testing_second_name)
            
        assert first_models.id== second_models.id
    
    def test_delete_by_ModelBaseService(self):
        model_to_delete="model to delete "
        
        create_model= MockModelBase.add_model(
            MockModelBase(name=model_to_delete)
        )
        create_model_id= create_model.id
        test_find_model=MockModelBase\
            .session\
            .query(MockModelBase)\
            .filter(MockModelBase.id == create_model_id)\
            .first()
        assert test_find_model != None
        
        MockModelBase.delete_model(create_model)
        testing_model=MockModelBase\
            .session\
            .query(MockModelBase)\
            .filter(MockModelBase.id==create_model_id)\
            .first()
        
        
        assert testing_model == None

    def test_model_can_delete_all_model(self):
        """test_model_can_delete_all_model
        """
        name_list= ["name one", "name two", "name three"]
        model_list:list[MockModelBase]= map(
            lambda name:MockModelBase(name= name),
            name_list
        )
        MockModelBase.add_all_model(model_list)
        MockModelBase.clean_all_model()
        all_model:list[MockModelBase]=MockModelBase\
            .session.query(MockModelBase).all()
        assert len(all_model) == 0