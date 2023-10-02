import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import cross_origin


DATA_DIRPATH = "../photo-match-data"
DATA_JSON_PATH = os.path.join(DATA_DIRPATH, "data.json")


app = Flask(__name__)


_data = None


def _get_data():
    global _data
    if _data is None:
        with open(DATA_JSON_PATH, "r") as f:
            _data = json.loads(f.read())
    
    return _data


def _set_data(data):
    global _data
    _data = data
    with open(DATA_JSON_PATH, "w") as f:
        f.write(json.dumps(
            data,
            indent=4,
            sort_keys=True))
    

@app.route("/data", methods=["GET"])
@cross_origin()
def get_data():
    """
    Gets JSON data from the datastore.
    """
    return jsonify(_get_data())


@app.route("/data", methods=["POST"])
@cross_origin()
def post_data():
    """
    Saves JSON data to the datastore.
    """
    data = _get_data()
    new_data = request.get_json()

    if new_data["_metadata"]["version"] <= data["_metadata"]["version"]:
        return jsonify({"error": "Invalid version"}), 400

    _set_data(data=new_data)

    return jsonify({"ok": True})


@app.route("/file/<filename>", methods=["GET"])
@cross_origin()
def get_file(filename):
    """
    Serves a file.
    """
    return send_from_directory(DATA_DIRPATH, filename)
