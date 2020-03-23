from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    """table of users' applications"""

    __tablename__ = 'applications'

    application_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    job_id = db. Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=True)
    datetime_applied = db.Column(db.DateTime, nullable=True)
    referred_by = db.Column(db.VARCHAR(length=1000), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=False)
    # TODO: # react-chartjs-2
    # using moment.js library, store as string w/ method .toString()
    # let time = moment()
    # time.toString() -> "Sat Mar 21 2020 20:37:27 GMT-0700"
    # parse in python: date1 = datetime.strptime("Sat Mar 21 2020 20:37:27 GMT-0700", "%a %b %d %Y %X %Z%z")
    # date1.strftime("%a %b %d %Y %X %Z%z") -> 'Sat Mar 21 2020 20:37:27 GMT-0700'
    # use TIMESTAMP sqlalchemy type

    user = db.relationship('User', 
                            backref='applications')
    job = db.relationship('Job', 
                            backref='applications')

    # TODO: look into cascade deletion

class ApplicationStatus(db.Model):
    """logs changes in Application status"""

    __tablename__ = 'application_statuses'

    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)
    status = db.Column(db.VARCHAR(length=1000), nullable=True)
    experience_rating = db.Column(db.VARCHAR(length=1000), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=False)

    application = db.relationship('Application',
                                    backref='application_statuses')

class JournalEntry(db.Model):
    """table for journal entries for an application"""

    __tablename__ = 'journal_entries'

    journal_entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)
    entry = db.Column(db.VARCHAR, nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False)

    application = db.relationship('Application',
                                    backref='journal_entries')

class Job(db.Model):
    """Table of specific job posts"""

    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    title = db.Column(db.VARCHAR(length=1000), nullable=False)
    link = db.Column(db.VARCHAR(length=1000), nullable=False)
    source = db.Column(db.VARCHAR(length=1000), nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False)

    company = db.relationship('Company', 
                                backref='jobs')

class Company(db.Model):

    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.VARCHAR(length=1000), nullable=False)
    website = db.Column(db.VARCHAR(length=1000), nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    """Table of users"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.VARCHAR(length=1000), nullable=False)
    password = db.Column(db.VARCHAR(length=20), nullable=False)
    first_name = db.Column(db.VARCHAR, nullable=False)
    last_name = db.Column(db.VARCHAR, nullable = False)
    points_total = db.Column(db.Integer, nullable=False, default=0)
    datetime_created = db.Column(db.DateTime, nullable=False)

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