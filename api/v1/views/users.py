#!/usr/bin/python3
"""
The route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Function retrieves all User objects
    :return: json of all users
    """
    userList = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        userList.append(obj.to_json())

    return jsonify(userList)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Function create user route
    :return: newly created user obj
    """
    userJson = request.get_json(silent=True)
    if userJson is None:
        abort(400, 'Not a JSON')
    if "email" not in userJson:
        abort(400, 'Missing email')
    if "password" not in userJson:
        abort(400, 'Missing password')

    new_user = User(**userJson)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    Function gets a specific User object by ID
    :param user_id: user object id
    :return: user obj with the specified id or error
    """

    fetchedObj = storage.get("User", str(user_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Function that updates specific User object by ID
    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure
    """
    userJson = request.get_json(silent=True)

    if userJson is None:
        abort(400, 'Not a JSON')

    fetchedObj = storage.get("User", str(user_id))

    if fetchedObj is None:
        abort(404)

    for key, val in userJson.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetchedObj, key, val)

    fetchedObj.save()

    return jsonify(fetchedObj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Function deletes User by id
    :param user_id: user object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("User", str(user_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})
