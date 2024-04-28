#!/usr/bin/python3
"""
The route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Function that retrieves all State objects
    :return: json of all states
    """
    stateList = []
    stateObj = storage.all("State")
    for obj in stateObj.values():
        stateList.append(obj.to_json())

    return jsonify(stateList)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    FUnction that create state route
    :return: newly created state obj
    """
    stateJson = request.get_json(silent=True)
    if stateJson is None:
        abort(400, 'Not a JSON')
    if "name" not in stateJson:
        abort(400, 'Missing name')

    newState = State(**stateJson)
    newState.save()
    resp = jsonify(newState.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Function gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """

    fetchedObj = storage.get("State", str(state_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Function that updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    stateJson = request.get_json(silent=True)
    if stateJson is None:
        abort(400, 'Not a JSON')
    fetchedObj = storage.get("State", str(state_id))
    if fetchedObj is None:
        abort(404)
    for key, val in stateJson.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetchedObj, key, val)
    fetchedObj.save()
    return jsonify(fetchedObj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Function that deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("State", str(state_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})
