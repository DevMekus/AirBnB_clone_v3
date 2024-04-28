#!/usr/bin/python3
"""
The route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    Function get all amenities of a place
    :param place_id: amenity id
    :return: all amenities
    """
    fetchedObj = storage.get("Place", str(place_id))

    allAmenities = []

    if fetchedObj is None:
        abort(404)

    for obj in fetchedObj.amenities:
        allAmenities.append(obj.to_json())

    return jsonify(allAmenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Function that unlinks an amenity in a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetchedObj = storage.get("Place", place_id)
    found = 0

    for obj in fetchedObj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetchedObj.amenities.remove(obj)
            else:
                fetchedObj.amenity_ids.remove(obj.id)
            fetchedObj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Function links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """

    fetchedObj = storage.get("Place", str(place_id))
    amenityObj = storage.get("Amenity", str(amenity_id))
    foundAmenity = None

    if not fetchedObj or not amenityObj:
        abort(404)

    for obj in fetchedObj.amenities:
        if str(obj.id) == amenity_id:
            foundAmenity = obj
            break

    if foundAmenity is not None:
        return jsonify(foundAmenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetchedObj.amenities.append(amenityObj)
    else:
        fetchedObj.amenities = amenityObj

    fetchedObj.save()

    resp = jsonify(amenityObj.to_json())
    resp.status_code = 201

    return resp
