#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    Function retrieves all Review objects by place
    :return: json of all reviews
    """
    reviewList = []
    placeObj = storage.get("Place", str(place_id))

    if placeObj is None:
        abort(404)

    for obj in placeObj.reviews:
        reviewList.append(obj.to_json())

    return jsonify(reviewList)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """
    Function create Review route
    :return: newly created Review obj
    """
    reviewJson = request.get_json(silent=True)
    if reviewJson is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", reviewJson["user_id"]):
        abort(404)
    if "user_id" not in reviewJson:
        abort(400, 'Missing user_id')
    if "text" not in reviewJson:
        abort(400, 'Missing text')

    reviewJson["place_id"] = place_id

    newReview = Review(**reviewJson)
    newReview.save()
    resp = jsonify(newReview.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    Function that gets a specific Review object by ID
    :param review_id: place object id
    :return: review obj with the specified id or error
    """

    fetchedObj = storage.get("Review", str(review_id))

    if fetchedObj is None:
        abort(404)

    return jsonify(fetchedObj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    Function that updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure
    """
    placeJson = request.get_json(silent=True)

    if placeJson is None:
        abort(400, 'Not a JSON')

    fetchedObj = storage.get("Review", str(review_id))

    if fetchedObj is None:
        abort(404)

    for key, val in placeJson.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetchedObj, key, val)

    fetchedObj.save()

    return jsonify(fetchedObj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    Function that deletes Review by id
    :param : Review object id
    :return: empty dict with 200 or 404 if not found
    """

    fetchedObj = storage.get("Review", str(review_id))

    if fetchedObj is None:
        abort(404)

    storage.delete(fetchedObj)
    storage.save()

    return jsonify({})
