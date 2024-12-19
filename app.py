from flask import Flask, render_template, request
from data import get_timeline_data, add_timeline_entry
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

if __name__ == '__main__':
    app.run(debug=True)
