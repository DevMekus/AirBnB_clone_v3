#!/usr/bin/python3
"""
The route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    Function retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    cityList = []
    stateObj = storage.get("State", state_id)

    if stateObj is None:
        abort(404)
    for obj in stateObj.cities:
        cityList.append(obj.to_json())

    return jsonify(cityList)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    Function create city route
    param: state_id - state id
    :return: newly created city obj
    """
    cityJson = request.get_json(silent=True)
    if cityJson is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in cityJson:
        abort(400, 'Missing name')

    cityJson["state_id"] = state_id

    newCity = City(**cityJson)
    newCity.save()
    resp = jsonify(newCity.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    Function gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    fetchedObj = storage.get("City", str(city_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    Function updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    cityJson = request.get_json(silent=True)
    if cityJson is None:
        abort(400, 'Not a JSON')
    fetchedObj = storage.get("City", str(city_id))
    if fetchedObj is None:
        abort(404)
    for key, val in cityJson.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetchedObj, key, val)
    fetchedObj.save()
    return jsonify(fetchedObj.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Function deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("City", str(city_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})
