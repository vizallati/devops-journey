import hashlib
import os
from flask import Flask, render_template, request, redirect, url_for, session
from app_utils import check_user_auth
from data import get_timeline_data, add_timeline_entry, get_recent_timeline_entries
from loguru import logger


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/devops-journey')
def devops_timeline():
    timeline_data = get_timeline_data(timeline='devops')
    return render_template('devops-timeline.html', timeline_data=timeline_data)

@app.route('/add-timeline-entry', methods=['POST'])
def add_entry():
    entry_data = request.json
    logger.info(entry_data)
    request_data = []
    for k,v in entry_data.items():
        request_data.append(v)
    add_timeline_entry(request_data, timeline=entry_data['timeline'])
    return f"{entry_data['timeline']} timeline entry successfully added"

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['loggedin'] = False
    if request.method == 'GET':
        return render_template('login.html', msg='')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if username and password == "allati":
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Wrong username or password"

@app.route('/test-automation-journey')
def aqa_timeline():
    timeline_data = get_timeline_data(timeline='aqa')
    return render_template('aqa-timeline.html', timeline_data=timeline_data)

@app.route('/dashboard')
def dashboard():
    if not check_user_auth():
        return redirect(url_for('login'))
    timeline_entries = get_timeline_data('devops')
    recent_timeline_data = get_recent_timeline_entries('devops')
    total_timeline_entries = len(timeline_entries)
    return render_template('dashboard.html',
                           recent_timeline_data=recent_timeline_data,
                           total_timeline_entries=total_timeline_entries)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/activity-feed')
def activity_feed():
    return render_template('activity-feed.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/other-interests')
def other_interests():
    return render_template('other-interests.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
