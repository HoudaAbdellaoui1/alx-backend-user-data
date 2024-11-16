#!/usr/bin/env python3
""" Module of User views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Retrieves all User objects.
    Return:
        - A JSON response containing a list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Retrieves a specific User object.

    Path parameter:
        - user_id (str): The ID of the User.
    Return:
        - A JSON response containing the User object.
        - 404 error if the User ID doesn't exist or if user_id is 'me' and no authenticated user is found.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/<user_id>
    Deletes a specific User object.

    Path parameter:
        - user_id (str): The ID of the User.
    Return:
        - An empty JSON response if the User is successfully deleted.
        - 404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/
    Creates a new User object.

    JSON body:
        - email (str): The email address of the User (required).
        - password (str): The password for the User (required).
        - first_name (str): The first name of the User (optional).
        - last_name (str): The last name of the User (optional).
    Return:
        - A JSON response containing the created User object.
        - 400 error if the input data is invalid or the User cannot be created.
    """
    rj = None
    error_msg = None

    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = f"Can't create User: {e}"
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/<user_id>
    Updates a specific User object.

    Path parameter:
        - user_id (str): The ID of the User.
    JSON body:
        - first_name (str): The updated first name of the User (optional).
        - last_name (str): The updated last name of the User (optional).
    Return:
        - A JSON response containing the updated User object.
        - 404 error if the User ID doesn't exist.
        - 400 error if the input data is invalid.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    rj = None
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
