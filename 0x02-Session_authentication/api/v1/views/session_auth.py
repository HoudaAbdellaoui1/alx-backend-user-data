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
    session = auth.create_session(user[0].id)
    response = make_response(jsonify(user[0].to_json()))
    response.set_cookie(getenv('SESSION_NAME'), session)

    return response
