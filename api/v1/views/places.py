#!/usr/bin/python3
"""
The route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    Function retrieves all Place objects by city
    :return: json of all Places
    """
    placeList = []
    cityObj = storage.get("City", str(city_id))
    for obj in cityObj.places:
        placeList.append(obj.to_json())

    return jsonify(placeList)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    Function create place route
    :return: newly created Place obj
    """
    placeJson = request.get_json(silent=True)
    if placeJson is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", placeJson["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in placeJson:
        abort(400, 'Missing user_id')
    if "name" not in placeJson:
        abort(400, 'Missing name')

    placeJson["city_id"] = city_id

    newPlace = Place(**placeJson)
    newPlace.save()
    resp = jsonify(newPlace.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    Function that gets a specific Place object by ID
    :param place_id: place object id
    :return: place obj with the specified id or error
    """

    fetchedObj = storage.get("Place", str(place_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    Function updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    placeJson = request.get_json(silent=True)

    if placeJson is None:
        abort(400, 'Not a JSON')

    fetchedObj = storage.get("Place", str(place_id))

    if fetchedObj is None:
        abort(404)

    for key, val in placeJson.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetchedObj, key, val)

    fetchedObj.save()

    return jsonify(fetchedObj.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Function deletes Place by id
    :param place_id: Place object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("Place", str(place_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})