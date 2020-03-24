from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data_1, example_data_2, example_data_3, example_data_4

class FlaskTestsDatabase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///jobstestdb')

        db.create_all()
        example_data_1()
        example_data_2()
        example_data_3()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_companies(self):
        result = self.client.get('/companies')
        self.assertIn(b'My Company', result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()