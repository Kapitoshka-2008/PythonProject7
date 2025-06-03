"""Flask application for the finance analyzer."""

from datetime import datetime

from flask import Flask

from .views import events_page, main_page

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    """Main page route."""
    return main_page(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.route("/events")
@app.route("/events/<period>")
def events(period="M"):
    """Events page route."""
    return events_page(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), period)


if __name__ == "__main__":
    app.run(debug=True) 