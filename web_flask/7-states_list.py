#!/usr/bin/python3
"""Start a Flask web application for states list.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display a list of states
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Close the database session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
