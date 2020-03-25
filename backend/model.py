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

    application_status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)
    status = db.Column(db.VARCHAR(length=1000), nullable=True)
    experience_rating = db.Column(db.VARCHAR(length=1000), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=False)

    application = db.relationship('Application',
                                    backref='application_statuses')
    point_entry = db.relationship('PointEntry',
                                    back_populates='application_status', 
                                    uselist=False)

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

class PointEntry(db.Model):
    """Table to log points earned"""

    __tablename__ = 'point_entries'

    point_entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    application_status_id = db.Column(db.Integer, db.ForeignKey('application_statuses.application_status_id'), unique=True, nullable=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)
    point_entry_type_id = db.Column(db.Integer, db.ForeignKey('point_entry_types.point_entry_type_id'), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=False)

    application_status = db.relationship('ApplicationStatus',
                                            back_populates='point_entry', 
                                            uselist=False)
    application = db.relationship('Application',
                                    backref='point_entries')
    point_entry_type = db.relationship('PointEntryType',
                                        backref='point_entries')

class PointEntryType(db.Model):
    """Different ways to earn points"""

    __tablename__ = 'point_entry_types'

    point_entry_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    point_entry_type_code = db.Column(db.VARCHAR(length=3), nullable=True)
    point_entry_type = db.Column(db.VARCHAR(length=1000), nullable=True)
    points = db.Column(db.Integer, nullable=True)

class Badge(db.Model):
    """Table to log badges earned"""

    __tablename__ = 'badges'

    badge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    badge_type_id = db.Column(db.Integer, db.ForeignKey('badge_types.badge_type_id'), nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User',
                            backref='badges')
    badge_type = db.relationship('BadgeType',
                                    backref='badges')

class BadgeType(db.Model):
    """Different ways to earn badges"""

    __tablename__ = 'badge_types'

    badge_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    badge_type = db.Column(db.VARCHAR(length=1000), nullable=True)


#########################################
#         seed & sample data            #
#########################################

def seed_types():
    """fill the PointEntryType & BadgeType tables"""

    # types of ways to earn points
    point_type1 = PointEntryType(point_entry_type_code='dli',
                            point_entry_type='Daily log-in',
                            points=1)
    point_type2 = PointEntryType(point_entry_type_code='uas', 
                            point_entry_type='Update application status',
                            points=1)
    point_type3 = PointEntryType(point_entry_type_code='gar',
                            point_entry_type='Got a referral',
                            points=2)
    point_type4 = PointEntryType(point_entry_type_code='a5j', 
                            point_entry_type='Applied to 5 jobs in a day',
                            points=5)
    db.session.add_all([point_type1, point_type2, point_type3, point_type4])
    
    # types of badges
    badge_type1 = BadgeType(badge_type='Every 100 points')
    badge_type2 = BadgeType(badge_type='Every 100 applications')
    db.session.add_all([badge_type1, badge_type2])

    db.session.commit()

def example_data_1():
    datetime_applied, datetime_created = datetime.now(), datetime.now()

    user = User(email='email@email.com', 
                password='password', 
                first_name='First', 
                last_name='Last', 
                datetime_created=datetime_created)
    db.session.add(user)

    company = Company(company_name='My Company', 
                        website='www.mycompany.com', 
                        datetime_created=datetime_created)
    db.session.add(company)
    db.session.commit()

    job = Job(company_id=company.company_id,
                title='Software Engineer',
                link='www.linkedin.com/mycompany/software-engineer',
                source='LinkedIn',
                datetime_created=datetime_created
                )
    db.session.add(job)
    db.session.commit()

    application = Application(user_id=user.user_id,
                                job_id=job.job_id,
                                datetime_applied=datetime_applied, 
                                referred_by="Anjelica", 
                                datetime_created=datetime_created)
    db.session.add(application)
    db.session.commit()

    application_status = ApplicationStatus(application_id=application.application_id,
                                            status='Applied',
                                            experience_rating='positive',
                                            datetime_created=datetime_created)
    db.session.add(application_status)
    db.session.commit()

    point_entry_type = db.session.query(PointEntryType).filter(PointEntryType.point_entry_type_code=='uas').first()
    point_entry = PointEntry(datetime_created=datetime_created)
    point_entry.application_status = application_status
    point_entry_type.point_entries.append(point_entry)
    db.session.add(point_entry)


    journal_entry = JournalEntry(application_id=application.application_id,
                            entry='This is a journal entry.',
                            datetime_created=datetime_created)

    db.session.add(journal_entry)
    db.session.commit()

def example_data_2():
    """add application"""
    datetime_applied, datetime_created = datetime.now(), datetime.now()

    user = User.query.first()

    company = db.session.query(Company).filter(Company.company_name.like('%Another Company%')).first()
    if not company:
        company = Company(company_name='Another Company', 
                            website='www.anothercompany.com', 
                            datetime_created=datetime_created)
    db.session.add(company)
    db.session.commit()

    job = db.session.query(Job).filter(Job.company_id==company.company_id, Job.title.like('%Software Engineer%')).first()
    if not job:
        job = Job(company_id=company.company_id,
                    title='Software Engineer',
                    link='www.linkedin.com/anothercompany/software-engineer',
                    source='Glassdoor',
                    datetime_created=datetime_created)
    db.session.add(job)
    db.session.commit()

    application = Application(user_id=user.user_id,
                                job_id=job.job_id,
                                datetime_applied=datetime_applied, 
                                referred_by="Anjelica", 
                                datetime_created=datetime_created)
    db.session.add(application)
    db.session.commit()

    application_status = ApplicationStatus(application_id=application.application_id,
                                            status='Applied',
                                            experience_rating='positive',
                                            datetime_created=datetime_created)
    db.session.add(application_status)

    journal_entry = JournalEntry(application_id=application.application_id,
                            entry='Another journal entry.',
                            datetime_created=datetime_created)

    db.session.add(journal_entry)
    db.session.commit()

def example_data_3():
    """add journal entry and new application status to 1st application"""
    journal_entry = JournalEntry(application_id=1,
                                entry='2nd journal entry to 1st application',
                                datetime_created = datetime.now()
                                )
    db.session.add(journal_entry)

    application_status = ApplicationStatus(application_id=Application.query.get(1).application_id,
                                            status='Phone Interviewed',
                                            experience_rating='neutral',
                                            datetime_created=datetime.now())
    db.session.add(application_status)
    db.session.commit()

def seed():
    seed_types()
    example_data_1()
    example_data_2()
    example_data_3()

def connect_to_db(app, db_uri='postgresql:///jobs'):
    """Configure and connect to psql after createdb database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
    print("CONNECTED TO DATABASE")