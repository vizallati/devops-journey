import hashlib
from flask import Flask, render_template, request, redirect, url_for
from data import get_timeline_data, add_timeline_entry, get_recent_timeline_entries
from loguru import logger

app = Flask(__name__)

@app.route('/')
def timeline():
    timeline_data = get_timeline_data()
    return render_template('devops-timeline.html', timeline_data=timeline_data)

@app.route('/add-timeline-entry', methods=['POST'])
def add_entry():
    entry_data = request.json
    logger.info(entry_data)
    request_data = []
    for k,v in entry_data.items():
        request_data.append(v)
    add_timeline_entry(request_data)
    return "Timeline entry successfully added"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', msg='')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        # hash = password + app.secret_key
        # hash = hashlib.sha1(hash.encode())
        # password = hash.hexdigest()
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    timeline_entries = get_timeline_data()
    recent_timeline_data = get_recent_timeline_entries()
    total_timeline_entries = len(timeline_entries)
    return render_template('dashboard.html',
                           recent_timeline_data=recent_timeline_data,
                           total_timeline_entries=total_timeline_entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
