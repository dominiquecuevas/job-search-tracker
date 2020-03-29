from unittest import TestCase
from server import app
from model import connect_to_db, db, seed, User

class FlaskTestsDatabase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///jobstestdb')

        db.create_all()
        seed()
        self.client.post('/login',
            data={'email': 'email@email.com', 'password': 'password'},
            follow_redirects=True
            )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_user(self):
        result = self.client.get('/user')
        self.assertIn(b'applications', result.data)

    def test_application(self):
        result = self.client.get('/application/1')
        self.assertIn(b'application_statuses', result.data)
    
    def test_application_status(self):
        result = self.client.get('/application_status/1')
        self.assertIn(b'Applied', result.data)

    def test_journal_entry(self):
        result = self.client.get('/journal_entry/2')
        self.assertIn(b'Another journal entry', result.data)

    def test_job(self):
        result = self.client.get('/job/1')
        self.assertIn(b'www.linkedin.com/mycompany/software-engineer', result.data)
    
    def test_company(self):
        result = self.client.get('company/1')
        self.assertIn(b'My Company', result.data)

    def test_point_entries(self):
        result = self.client.get('/point_entries')
        self.assertIn(b'/point_entry_type/2', result.data)

    def test_point_entry_type(self):
        result = self.client.get('/point_entry_type/2')
        self.assertIn(b'uas', result.data)
    
    def test_badges(self):
        result = self.client.get('/badges')
        self.assertIn(b'100 points', result.data)

    def test_badge_type(self):
        result = self.client.get('/badge_type/1')
        self.assertIn(b'100 points', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()