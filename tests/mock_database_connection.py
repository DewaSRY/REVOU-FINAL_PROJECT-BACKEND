
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model_base_service import  db,ModelBaseService

engine = create_engine("sqlite:///tests/data.db")
Session = sessionmaker(bind=engine)
SESSION = Session()

class MockDatabaseConnection(TestCase): 
    "Mock class use to simulation the testing case"
    def setup_class(self):
        db.Model.metadata.create_all(engine)
        self.session= SESSION
        ModelBaseService.set_session(SESSION)
        
    def teardown_class(self):
        self.session.rollback()
        self.session.close()
