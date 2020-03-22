from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Application(db.Model):
    """table of users' applications"""

    __tablename__ = 'applications'

    application_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    job_id = db. Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=True)
    datetime_applied = db.Column(db.DateTime, nullable=True)
    referred_by = db.Column(db.VARCHAR(length=1000), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=True)
    # TODO: # react-chartjs-2
    # using moment.js library, store as string w/ method .toString()
    # let time = moment()
    # time.toString() -> "Sat Mar 21 2020 20:37:27 GMT-0700"
    # parse in python: date1 = datetime.strptime("Sat Mar 21 2020 20:37:27 GMT-0700", "%a %b %d %Y %X %Z%z")
    # date1.strftime("%a %b %d %Y %X %Z%z") -> 'Sat Mar 21 2020 20:37:27 GMT-0700'
    # use TIMESTAMP sqlalchemy type

    user = db.relationship('User', backref='applications')
    job = db.relationship('Job', backref='jobs')

class Job(db.Model):
    """Table of specific job posts"""

    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    title = db.Column(db.VARCHAR(length=1000), nullable=False)
    link = db.Column(db.VARCHAR(length=1000), nullable=False)
    source = db.Column(db.VARCHAR(length=1000), nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=True)

class User(db.Model):
    """Table of users"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.VARCHAR(length=1000), nullable=False)
    password = db.Column(db.VARCHAR(length=20), nullable=False)
    first_name = db.Column(db.VARCHAR, nullable=False)
    last_name = db.Column(db.VARCHAR, nullable = False)
    points_total = db.Column(db.Integer, nullable=False, default=0)
    datetime_created = db.Column(db.DateTime, nullable=True)

def seed():
    datetime_applied, datetime_created = datetime.now(), datetime.now()
    application = Application(datetime_applied=datetime_applied, referred_by="Anjelica", datetime_created=datetime_created)
    db.session.add(application)
    db.session.commit()

def connect_db(app):
    """Configure and connect to psql after createdb database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app
    connect_db(app)
    db.create_all()
    print("CONNECTED TO DATABASE")