from datetime import datetime
import pty
import os
import subprocess
from flask_socketio import SocketIO
import select
import termios
import struct
import fcntl
import shlex
import logging
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
app.config["fd"] = None
app.config["child_pid"] = None
from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins=["https://blog.vizallati.guru"])

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
    return jsonify({'message': 'Activity added successfully!', 'activity_id': activity_id}),



def set_winsize(fd, row, col, xpix=0, ypix=0):
    logging.debug("setting window size with termios")
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if app.config["fd"]:
            timeout_sec = 0
            (data_ready, _, _) = select.select([app.config["fd"]], [], [], timeout_sec)
            if data_ready:
                output = os.read(app.config["fd"], max_read_bytes).decode(
                    errors="ignore"
                )
                socketio.emit("pty-output", {"output": output}, namespace="/playground")


@app.route("/playground")
def playground():
    return render_template("playground.html")


@socketio.on("pty-input", namespace="/playground")
def pty_input(data):
    """write to the child pty. The pty sees this as if you are typing in a real
    terminal.
    """
    if app.config["fd"]:
        logger.debug("received input from browser: %s" % data["input"])
        os.write(app.config["fd"], data["input"].encode())


@socketio.on("resize", namespace="/playground")
def resize(data):
    if app.config["fd"]:
        logger.debug(f"Resizing window to {data['rows']}x{data['cols']}")
        set_winsize(app.config["fd"], data["rows"], data["cols"])


@socketio.on("connect", namespace="/playground")
def connect():
    """new client connected"""
    logger.info("new client connected")
    if app.config["child_pid"]:
        # already started child process, don't start another
        return

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run(app.config["cmd"])
    else:
        # this is the parent process fork.
        # store child fd and pid
        app.config["fd"] = fd
        app.config["child_pid"] = child_pid
        set_winsize(fd, 50, 50)
        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
        # logging/print statements must go after this because... I have no idea why
        # but if they come before the background task never starts
        socketio.start_background_task(target=read_and_forward_pty_output)

        logger.info("child pid is " + child_pid)
        logger.info(
            f"starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
        logger.info("task started")

if __name__ == '__main__':
    app.config["cmd"] = 'bash'
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
