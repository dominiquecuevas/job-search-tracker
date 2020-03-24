from unittest import TestCase
from server import app
from model import connect_to_db, db, seed

class FlaskTestsDatabase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///jobstestdb')

        db.create_all()
        seed()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_companies(self):
        result = self.client.get('/companies')
        self.assertIn(b'My Company', result.data)
        self.assertIn(b'Another Company', result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()