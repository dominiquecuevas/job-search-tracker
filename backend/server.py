from flask import Flask, jsonify
import time

app = Flask(__name__)
app.secret_key = 'yliwmhd'

@app.route('/time')
def homepage():
    return jsonify({'time': time.time()})

if __name__ == "__main__":
    # connect_db(app)
    # db.create_all()
    
    app.run(host="0.0.0.0", debug=True)