from datetime import datetime
from model import Application, Job, Company, JournalEntry, User, connect_db, db
from server import app
import pprint

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

    journalentry = JournalEntry(application_id=application.application_id,
                            entry='This is a journal entry.',
                            datetime_created=datetime_created)

    db.session.add(journalentry)
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

    journalentry = JournalEntry(application_id=application.application_id,
                            entry='Another journal entry.',
                            datetime_created=datetime_created)

    db.session.add(journalentry)
    db.session.commit()

def seed3():
    """add journal entry to 1st application"""
    journalentry = JournalEntry(application_id=1,
                                entry='2nd journal entry to 1st application',
                                datetime_created = datetime.now()
                                )
    db.session.add(journalentry)
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

    return pprint.pprint(
                    {'jobs': jobs,
                    'company': company,
                    'users': users,
                    'companies': companies
                    }
    )

if __name__ == "__main__":
    connect_db(app)
    db.create_all()