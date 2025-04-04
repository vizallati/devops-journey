import hashlib
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from markupsafe import Markup

from app_utils import check_user_auth, convert_rrs_to_json, summarize_article
from data import get_timeline_data, add_timeline_entry, get_recent_timeline_entries, add_project_entry, get_projects, \
    get_search_query, add_activity_entry, get_activity_entries
from loguru import logger

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = '/app/static/images'     #Need to change this when debugging locally
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEFAULT_FILTER = 'aqa'


@app.route('/')
def home():
    return redirect(url_for('get_categories', category=DEFAULT_FILTER))

@app.route('/devops-journey')
def devops_timeline():
    timeline_data = get_timeline_data(timeline='devops')
    return render_template('devops-timeline.html', timeline_data=timeline_data)

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
    all_project_entries = get_projects()
    return render_template('projects.html', projects=all_project_entries)

@app.route('/activity-feed')
def activity_feed():
    activities = get_activity_entries()
    return render_template('activity-feed.html', activities=activities)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/other-interests')
def other_interests():
    return render_template('other-interests.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(directory='static', path='sitemap.xml')

@app.route('/categories')
def get_categories():
    category = request.args.get('category')
    match category:
        case 'aqa' | 'devops':
            timeline_data = get_timeline_data(timeline=category)
            return render_template('index.html', timeline_data=timeline_data)
        case 'projects':
            all_project_entries = get_projects()
            return render_template('index.html', projects=all_project_entries)
        case _:
            return render_template('index.html')

@app.route('/articles')
def articles():
    json_data = convert_rrs_to_json()
    logger.info(f"Medium feed data {json_data}")
    json_data[0]["description"] = summarize_article(json_data[0]["description"])
    json_data[0]["description"] = Markup(json_data[0]["description"].strip())
    logger.info(f'Article summary is: {json_data[0]["description"]}')
    return render_template('articles.html', feed_items=json_data)



###################### API ENDPOINTS ###########################################################

@app.route('/api/v1/search')
def search():
    query = request.args.get('search')
    results = get_search_query(query)
    if results:
        return render_template('index.html', search_results=results)
    else:
        return render_template('index.html', no_search_results=True)

@app.route('/api/v1/timeline', methods=['POST'])
def add_entry():
    entry_data = request.json
    logger.info(entry_data)
    request_data = []
    for k,v in entry_data.items():
        request_data.append(v)
    add_timeline_entry(request_data, timeline=entry_data['timeline'])
    return jsonify({"message": "Timeline entry successfully added","entry": entry_data['timeline']}), 201


@app.route('/api/v1/project', methods=['POST'])
def add_project():
    file = request.files['image']
    file_path = None
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    text_data = request.form
    logger.info(text_data)
    add_project_entry(file_path, text_data)
    return jsonify({"message": "Project entry successfully added"}), 201

@app.route('/api/v1/login', methods=['GET', 'POST'])
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

@app.route('/api/v1/activity', methods=['POST'])
def add_activity():
    photo = request.files['image']
    file_path = None
    if photo:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(file_path)
    activity_data = request.form
    logger.info(activity_data)
    description = activity_data.get('description')
    activity_date =  datetime.utcnow().date()
    activity_id = add_activity_entry(description, file_path, activity_date)
    return jsonify({'message': 'Activity added successfully!', 'activity_id': activity_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
