from flask import current_app as app
from flask import render_template
from app.api.departures import get_departures_data

@app.route("/api/departures")
def get_departures():
    return get_departures_data()

@app.route("/")
def index():
    return render_template("index.html")