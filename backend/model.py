from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Application(db.Model):
    """table of users' applications"""

    __tablename__ = 'applications'

    application_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    # job_id = db. Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=True)
    datetime_applied = db.Column(db.DateTime, nullable=True)
    referred_by = db.Column(db.Text, nullable=True)
    datetime_created = db.Column(db.DateTime, nullable=True)

def seed():
    # TODO: use javascript Date().getTime()
    # future scope using chartjs use momentjs library
        # now = moment() for client's locale time
        # change format now.format('x') for timestamp in milliseconds
        # or now.format('YYYY M D')
    # use TIMESTAMP sqlalchemy type
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