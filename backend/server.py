from flask import Flask, jsonify
import time
from model import db, connect_to_db, \
                    Application, ApplicationStatus, Job, Company, JournalEntry, \
                    User, PointEntry, PointEntryType, Badge, BadgeType

app = Flask(__name__)
app.secret_key = 'yliwmhd'

@app.route('/time')
def homepage():
    return jsonify({'time': time.time()})

@app.route('/companies')
def companies():
    companies = Company.query.all()
    companies_list = [company.company_name for company in companies]
    return jsonify({'companies': companies_list
    })


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    
    app.run(host="0.0.0.0", debug=True)