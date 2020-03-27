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
    print(email)
    print(password)
    user = db.session.query(User).filter(User.email==email).first()
    if user and user.check_password(password):
        print('logged in!')
        login_user(user)
        return jsonify({'message':'logged in'})
    else:
        flash('Your email or password was incorrect')
    # return redirect('/')


@app.route('/companies')
def companies():
    companies = Company.query.all()
    companies_list = [company.company_name for company in companies]
    return jsonify({'companies': companies_list
    })

@app.route('/application-statuses')
@login_required
def application_statuses():
    pass

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    
    app.run(host="0.0.0.0", debug=True)