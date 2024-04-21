#!/usr/bin/python3
"""list of state"""


from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states_list")
def lists():
    storage_new = []
    for states in storage.all(State).values():
        storage_new.append(states.sort())
    return render_template("7-states_list.html", states=storage_new)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
