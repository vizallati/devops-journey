from flask import Flask, render_template
from data import get_timeline_data

app = Flask(__name__)

@app.route('/')
def timeline():
    timeline_data = get_timeline_data()
    return render_template('devops-timeline.html', timeline_data=timeline_data)

if __name__ == '__main__':
    app.run(debug=True)
