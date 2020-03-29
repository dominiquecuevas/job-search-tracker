from flask import Flask, jsonify, session, request, flash
import time
from model import db, connect_to_db, \
                    Application, ApplicationStatus, Job, Company, JournalEntry, \
                    User, PointEntry, PointEntryType, Badge, BadgeType
from flask_login import LoginManager, login_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'yliwmhd'
login_manager = LoginManager(app)

@app.route('/time')
def homepage():
    return jsonify({'time': time.time()})

@login_manager.user_loader
def load_user(email):
    """This is used by flask_login to load the current user."""

    return db.session.query(User).filter(User.email==email).first()

@app.route('/login', methods=['POST'])
def log_in_user():
    """Log in a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter(User.email==email).first()
    if user and user.check_password(password):
        print('logged in!')
        login_user(user)
        return jsonify({'message':'logged in'})
    else:
        flash('Your email or password was incorrect')
    # return redirect('/')

@app.route('/user')
@login_required
def user():
    user = current_user
    return jsonify({
        'user_id': user.user_id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'points_total': user.points_total,
        'datetime_created': user.datetime_created,
        'applications': list(
            map(lambda application: f'/application/{application.application_id}',
            current_user.applications)
        )
    })

@app.route('/application/<int:application_id>')
@login_required
def get_application(application_id):
    # TODO: try and except for application_id not associated to current_user
    application = db.session \
        .query(Application) \
        .filter((Application.user==current_user) &
            (Application.application_id==application_id)) \
        .one()
    return jsonify({
        'application_id': application.application_id,
        'job': f'/job/{application.job_id}',
        'datetime_applied': application.datetime_created,
        'referred_by': application.referred_by,
        'datetime_created': application.datetime_created,
        'application_statuses': list(
            map(lambda application_status: f'/application_status/{application_status.application_status_id}', 
            application.application_statuses)
        ),
        'journal_entries': list(
            map(lambda journal_entry: f'/journal_entry/{journal_entry.journal_entry_id}', 
            application.journal_entries)
        )
    })

@app.route('/application_status/<int:application_status_id>')
@login_required
def application_statuses(application_status_id):
    application_status = db.session \
        .query(ApplicationStatus) \
        .join(Application, User) \
        .filter((Application.user==current_user) & 
            (ApplicationStatus.application_status_id==application_status_id)) \
        .one()
    return jsonify({
        'application': f'/application/{application_status.application_id}',
        'status': application_status.status,
        'experience_rating': application_status.experience_rating,
        'datetime_created': application_status.datetime_created,
    })

@app.route('/journal_entry/<int:journal_entry_id>')
@login_required
def journal_entry(journal_entry_id):
    journal_entry = db.session \
        .query(JournalEntry) \
        .join(Application) \
        .filter((Application.user==current_user) &
            (JournalEntry.journal_entry_id==journal_entry_id)) \
        .one()
    return jsonify({
        'application': f'/application/{journal_entry.application.application_id}',
        'entry': journal_entry.entry,
        'datetime_created': journal_entry.datetime_created,
    })

@app.route('/job/<int:job_id>')
@login_required
def get_job(job_id):
    job = db.session \
        .query(Job) \
        .join(Application) \
        .filter((Application.user==current_user) &
            (Job.job_id==job_id)) \
        .one()
    return jsonify({
        'company_id': f'/company/{job.company_id}',
        'title': job.title,
        'link': job.link,
        'source': job.source,
        'datetime_created': job.datetime_created,
    })

@app.route('/company/<int:company_id>')
@login_required
def get_company(company_id):
    company = db.session \
        .query(Company) \
        .join(Job, Application) \
        .filter((Application.user==current_user) &
            (Company.company_id==company_id)) \
        .one()
    return jsonify({
        'company_name': company.company_name,
        'website': company.website,
        'datetime_created': company.datetime_created,
    })

@app.route('/point_entries')
@login_required
def get_point_entries():
    point_entries = db.session \
        .query(PointEntry) \
        .join(ApplicationStatus, Application) \
        .filter(Application.user==current_user) \
        .all()
    return jsonify(list(
        map(lambda point_entry: {
            'application_status_id': point_entry.application_status_id,
            'application_id': point_entry.application_id,
            'point_entry_type': f'/point_entry_type/{point_entry.point_entry_type_id}',
            'datetime_created': point_entry.datetime_created,
            'points': point_entry.points,
        }, 
        point_entries)
    ))

@app.route('/point_entry_type/<int:point_entry_type_id>')
@login_required
def get_point_entry_type(point_entry_type_id):
    point_entry_type = db.session \
        .query(PointEntryType) \
        .filter(PointEntryType.point_entry_type_id==point_entry_type_id) \
        .one()
    return jsonify({
        'point_entry_type_code': point_entry_type.point_entry_type_code,
        'point_entry_type': point_entry_type.point_entry_type,
        'points': point_entry_type.points,
        })

@app.route('/badges')
@login_required
def get_badges():
    badges = db.session \
        .query(Badge) \
        .filter(Badge.user==current_user) \
        .all()
    return jsonify(list(
        map(lambda badge: {
            'badge_id': badge.badge_id,
            'user_id': badge.user_id,
            'badge_type': badge.badge_type.badge_type,
            'datetime_created': badge.datetime_created,
        }, badges)
    ))

@app.route('/badge_type/<int:badge_type_id>')
def get_badge_types(badge_type_id):
    badge_type = BadgeType.query.get(badge_type_id)
    return jsonify({
        'badge_type': badge_type.badge_type
    })

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    
    app.run(host="0.0.0.0", debug=True)