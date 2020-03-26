from flask import Flask, jsonify, session, request
import time
from model import db, connect_to_db, \
                    Application, ApplicationStatus, Job, Company, JournalEntry, \
                    User, PointEntry, PointEntryType, Badge, BadgeType
# from flask_login import LoginManager, login_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'yliwmhd'
# login_manager = LoginManager(app)

@app.route('/time')
def homepage():
    return jsonify({'time': time.time()})

@app.route('/login', methods=['POST'])
def log_in_user():
    # email = request.form['email']
    # password = request.form['password']
    # user = db.session.query(User)
    email = request.form.get('email')
    password = request.form.get('password')
    print('name, passord:', email, password)
    # return jsonify({'name': name})

@app.route('/companies')
def companies():
    companies = Company.query.all()
    companies_list = [company.company_name for company in companies]
    return jsonify({'companies': companies_list
    })

@app.route('/application-statuses')
def application_statuses():
    pass

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    
    app.run(host="0.0.0.0", debug=True)