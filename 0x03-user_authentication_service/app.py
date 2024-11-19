#!/usr/bin/env python3
"""Route module for the basic Flask app
"""
from flask import Flask
from flask.json import jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ Basic route
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

# from os import getenv
# from flask import Flask, jsonify, abort, request
# from flask_cors import (CORS, cross_origin)
# import os
# from api.v1.auth.auth import Auth
# from api.v1.auth.basic_auth import BasicAuth
# from api.v1.auth.session_auth import SessionAuth
# from api.v1.auth.session_exp_auth import SessionExpAuth
# from api.v1.auth.session_db_auth import SessionDBAuth
# from api.v1.views import app_views

# app = Flask(__name__)
# app.register_blueprint(app_views)
# CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# auth = None
# AUTH_CLASSES = {
#     'auth': Auth,
#     'basic_auth': BasicAuth,
#     'session_auth': SessionAuth,
#     'session_exp_auth': SessionExpAuth,
#     'session_db_auth': SessionDBAuth
# }
# auth_type = getenv('AUTH_TYPE')
# auth = AUTH_CLASSES.get(auth_type)()

# @app.errorhandler(404)
# def not_found(error) -> str:
#     """ Not found handler
#     """
#     return jsonify({"error": "Not found"}), 404


# @app.errorhandler(401)
# def unauthorized(error) -> str:
#     """ unauthorized handler
#     """
#     return jsonify({"error": "Unauthorized"}), 401


# @app.errorhandler(403)
# def forbidden(error) -> str:
#     """ forbidden handler
#     """
#     return jsonify({"error": "Forbidden"}), 403


# @app.before_request
# def before_request():
#     """ Filter requests before handling them.
#     """
#     request.current_user = auth.current_user(request)
#     if auth is None:
#         return

#     excluded = ['/api/v1/status/', '/api/v1/unauthorized/',
#                 '/api/v1/forbidden/', '/api/v1/auth_session/login/']
#     if not auth.require_auth(request.path, excluded):
#         return

#     if auth.authorization_header(request) is None and auth.session_cookie(
#             request) is None:
#         abort(401)

#     if auth.current_user(request) is None:
#         abort(403)

#     if auth.authorization_header(request) and auth.session_cookie(request):
#         abort(401)
#         return None


# if __name__ == "__main__":
#     host = getenv("API_HOST", "0.0.0.0")
#     port = getenv("API_PORT", "5000")
#     app.run(host=host, port=port)
