from unittest import TestCase
from server import app
from model import connect_to_db, db, seed, seed_types, User, Company, Job, Application, ApplicationStatus

class FlaskTestsDatabase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///jobstestdb')

        db.create_all()

        seed_types()
        user = User(email='email@email.com', 
            password='password', 
            first_name='First', 
            last_name='Last')
        db.session.add(user)
        db.session.commit()
        # TODO: reduce seed data in exchange for tests
        self.client.post('/login',
            data={'email': 'email@email.com', 'password': 'password'},
            follow_redirects=True
            )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_login(self):
        result = self.client.get('/logout')
        self.assertEqual(result.status_code, 200)

        result = self.client.post('/login',
            data={'email': 'email@email.com', 'password': 'password'},
            follow_redirects=True
        )
        self.assertEqual(result.status_code, 200)

        self.client.get('/logout')
        result = self.client.post('/login', 
            data={'email': 'email@email.com', 'password': 'wrong password'},
            follow_redirects=True
        )
        self.assertEqual(result.status_code, 401)

    def test_new_application(self):
        result = self.client.post('/new-application',
            data={'company_name': 'Company Name',
                  'website': 'https://www.company.com',
                  'title': 'Title',
                  'link': 'https://www.link.com',
                  'source': 'LinkedIn',
                  'status': 'Applied'
            }
        )
        self.assertEqual(result.status_code, 200)

        self.client.post('/new-application',
            data={'company_name': 'Second Company',
                  'website': 'https://www.secondcompany.com',
                  'title': 'Title',
                  'link': 'https://www.link.com',
                  'source': 'LinkedIn',
                  'status': 'Applied'
            }
        )
        self.client.post('/new-application',
            data={'company_name': 'Second Company',
                  'website': 'https://www.secondcompany.com',
                  'title': 'Second Title',
                  'link': 'https://www.secondlink.com',
                  'source': 'LinkedIn',
                  'status': 'Applied'
            }
        )
        result = db.session.query(Application).all()
        self.assertEqual(len(result), 3)
        result = db.session.query(Company).all()
        self.assertEqual(len(result), 2)
        result = db.session.query(Job).all()
        self.assertEqual(len(result), 3)

    def test_status_change(self):
        self.client.post('/new-application',
            data={'company_name': 'Company Name',
                  'website': 'https://www.company.com',
                  'title': 'Title',
                  'link': 'https://www.link.com',
                  'source': 'LinkedIn',
                  'status': 'Applied'
            }
        )
        application = db.session.query(Application).first()
        
        result = self.client.post('/new-application-status',
            data={
                'application_id': application.application_id,
                'new_status': 'Phone interviewed'
            }
        )
        self.assertEqual(result.status_code, 200)

        application = db.session.query(Application).first()
        application_statuses = application \
            .application_statuses \
            .order_by(ApplicationStatus.datetime_created.desc()) \
            .all()
        
        self.assertEqual(application_statuses[0].status, 'Phone interviewed')
        self.assertEqual(application_statuses[1].status, 'Applied')


if __name__ == "__main__":
    import unittest

    unittest.main()