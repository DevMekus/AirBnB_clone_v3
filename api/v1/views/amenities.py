#!/usr/bin/python3
"""
the route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Function retrieves all Amenity objects
    :return: json of all states
    """
    amlist = []
    amobj = storage.all("Amenity")
    for obj in amobj.values():
        amlist.append(obj.to_json())

    return jsonify(amlist)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Function create amenity route
    :return: newly created amenity obj
    """
    amjson = request.get_json(silent=True)
    if amjson is None:
        abort(400, 'Not a JSON')
    if "name" not in amjson:
        abort(400, 'Missing name')

    newam = Amenity(**amjson)
    newam.save()
    resp = jsonify(newam.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Function gets a specific Amenity object by ID
    :param amenity_id: amenity object id
    :return: state obj with the specified id or error
    """

    fetchedObj = storage.get("Amenity", str(amenity_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    Function updates specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: amenity object and 200 on success, 
    or 400 or 404 on failure
    """
    amJson = request.get_json(silent=True)
    if amJson is None:
        abort(400, 'Not a JSON')
    fetchedObj = storage.get("Amenity", str(amenity_id))
    if fetchedObj is None:
        abort(404)
    for key, val in amJson.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetchedObj, key, val)
    fetchedObj.save()
    return jsonify(fetchedObj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Function deletes Amenity by id
    :param amenity_id: Amenity object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("Amenity", str(amenity_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})
