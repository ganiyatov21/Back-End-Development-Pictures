from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((picture for picture in data if picture["id"] == id), None)
    if picture is None:
        return jsonify(Message=f"picture with id {id} not found"), 404
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not isinstance(picture, dict) or type(picture.get("id")) is not int:
        return jsonify(Message="A JSON picture with an integer id is required"), 400
    if any(existing["id"] == picture["id"] for existing in data):
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302
    required = {"pic_url", "event_country", "event_state", "event_city", "event_date"}
    if not required.issubset(picture):
        return jsonify(Message="Missing required picture fields"), 400
    data.append(dict(picture))
    response = jsonify(picture)
    response.status_code = 201
    response.headers["Location"] = url_for("get_picture_by_id", id=picture["id"])
    return response

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((picture for picture in data if picture["id"] == id), None)
    if picture is None:
        return jsonify(Message=f"picture with id {id} not found"), 404
    changes = request.get_json()
    if not isinstance(changes, dict) or ("id" in changes and changes["id"] != id):
        return jsonify(Message="Picture id must match the URL"), 400
    picture.update(changes)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((picture for picture in data if picture["id"] == id), None)
    if picture is None:
        return jsonify(Message=f"picture with id {id} not found"), 404
    data.remove(picture)
    return "", 204
