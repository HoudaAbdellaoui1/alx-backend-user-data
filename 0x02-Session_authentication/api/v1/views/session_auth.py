#!/usr/bin/env python3
"""Module of Session auth views."""
from os import getenv
from flask import abort, jsonify, request, make_response
from models.user import User

from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session = auth.create_session(getattr(user[0], 'id'))
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), session)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
