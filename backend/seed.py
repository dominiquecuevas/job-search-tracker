from datetime import datetime
from model import Application, ApplicationStatus, Job, Company, JournalEntry, \
                    User, PointEntry, PointEntryType, Badge, BadgeType, \
                    connect_to_db, db
from server import app
import pprint

def seed0():
    """fill the 'types' tables"""

    # types of ways to earn points
    point_type1 = PointEntryType(point_entry_type='Daily log-in',
                            points=1)
    point_type2 = PointEntryType(point_entry_type='Change application status',
                            points=1)
    point_type3 = PointEntryType(point_entry_type='Got referral',
                            points=2)
    point_type4 = PointEntryType(point_entry_type='Applied to 5 jobs in a day',
                            points=5)
    point_type5 = PointEntryType(point_entry_type='Sent Followup',
                            points=1)
    db.session.add_all([point_type1, point_type2, point_type3, point_type4, point_type5])
    
    # types of badges
    badge_type1 = BadgeType(badge_type='Every 100 points')
    badge_type2 = BadgeType(badge_type='Every 100 applications')
    db.session.add_all([badge_type1, badge_type2])

    db.session.commit()

def seed1():
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

    journal_entry = JournalEntry(application_id=application.application_id,
                            entry='This is a journal entry.',
                            datetime_created=datetime_created)

    db.session.add(journal_entry)
    db.session.commit()

def seed2():
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

def seed3():
    """add journal entry to 1st application"""
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

def query_seeds():
    # the jobs with their journalentry
    jobs = db.session.query(JournalEntry.datetime_created, Job.title, JournalEntry.entry, Company.company_name) \
                        .select_from(JournalEntry) \
                        .join(Application, Job, Company) \
                        .order_by(JournalEntry.datetime_created) \
                        .all()

    # get back the company the job queried was for
    company = Application.query.get(1).job.company

    # get back the users applied to 'Software Engineer'
    users = db.session.query(User) \
                        .join(Application, Job) \
                        .filter(Job.title.like('%Software Engineer%')) \
                        .all()

    # companies with search word in journal entry
    companies = db.session.query(Company.company_name) \
                            .join(Job, Application, JournalEntry) \
                            .filter(JournalEntry.entry.ilike('%another%')) \
                            .all()

    # get all application statuses for an application
    application_statuses = db.session.query(ApplicationStatus.datetime_created, 
                                            ApplicationStatus.status,
                                            Application.datetime_applied,
                                            Company.company_id) \
                                    .join(Application, Job, Company) \
                                    .order_by(ApplicationStatus.application_id,
                                                ApplicationStatus.datetime_created) \
                                    .all()

    # TODO: queries for BadgeType & PointEntryType

    return pprint.pprint(
                    {'jobs': jobs,
                    'company': company,
                    'users': users,
                    'companies': companies,
                    'application_statuses': application_statuses,
                    }
    )

def seed():
    seed0()
    seed1()
    seed2()
    seed3()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()